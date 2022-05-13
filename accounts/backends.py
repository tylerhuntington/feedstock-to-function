from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import CustomUser

class CustomUserBackend(BaseBackend):
    """
    Authenticate against CustomUser model
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = CustomUser.objects.get(email=username)
            pwd_valid = check_password(password, user.password)
            if pwd_valid:
                return user
        except CustomUser.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None