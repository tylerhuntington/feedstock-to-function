from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.views import login
from .models import CustomUser
from accounts.views import send_email_address_confirm_email_to_new_user
from django.http import HttpResponseRedirect


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    new_user_redir_url = '/accounts/confirm/'

    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        We're trying to solve different use cases:
        - social account already exists, just go on
        - social account has no email or email is unknown, just go on
        - social account's email exists, link social account to existing user
        """

        # some social logins don't have an email address, e.g. facebook accounts
        # with mobile numbers only, but allauth takes care of this case so just
        # ignore it
        if 'email' not in sociallogin.account.extra_data:
            return
        email = sociallogin.account.extra_data['email'].lower()

        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            return

        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        try:
            # if user exists, connect this new social login to the existing user
            # and try logging them in. If the account hasn't been activated yet
            # then login will fail and present an appropriate error message
            user = CustomUser.objects.get(email__iexact=email)
            sociallogin.connect(request, user)
            login(request)
            # pass

        # if it does not, let allauth take care of this new social account
        except CustomUser.DoesNotExist:
            pass

        pass

