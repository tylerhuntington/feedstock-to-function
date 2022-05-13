import secrets
from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from django.conf import settings
from django.core.mail import EmailMessage
import logging

# config logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(asctime)s %(levelname)s %(name)s] %(message)s', datefmt='%m-%d %H:%M'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in settings.ADMINS:
            user_email = user[1]
            u = CustomUser.objects.filter(email=user_email).first()
            if u:
                u.is_superuser = True
                u.is_staff = True
                u.is_admin = True
                u.is_active = True
                u.save()
            else:
                # create superuser account for the user in ADMINS list
                pw_length = 32
                pw = secrets.token_urlsafe(pw_length)
                logger.info(f'Creating superuser account for {user_email}')
                admin = CustomUser.objects.create_superuser(
                    email=user_email, password=pw
                )
                admin.is_active = True
                admin.is_admin = True
                admin.save()
                mail_subject = 'New Admin Account'
                message = f"Admin Password: {pw}"
                email = EmailMessage(
                    mail_subject, message, to=[user_email]
                )
                email.send()
