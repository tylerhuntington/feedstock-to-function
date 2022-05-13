from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    FIELD_OF_WORK_CHOICES = [
        ('', 'Field of Work'),
        ('industry', 'Industry'),
        ('private_consulting', 'Private Consulting'),
        ('academia', 'Academia/Education'),
        ('research', 'Research'),
        ('government', 'Government Agency'),
        ('nonprofit_org', 'Non-profit Organization'),
        ('other', 'Other'),
    ]

    username = None
    email = models.EmailField(
        _('Email Address'),
        unique=True,
    )

    affiliation = models.CharField(
        _('Organization/Company'),
        max_length=150,
    )

    field_of_work = models.CharField(
        _('Field of Work'),
        max_length=150,
        choices=FIELD_OF_WORK_CHOICES,
        default='',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):

        try:
            self.auth_token
            super().save(*args, **kwargs)
        except Token.DoesNotExist:
            super().save(*args, **kwargs)
            self.gen_api_token()

    def delete(self, *args, **kwargs):
        try:
            api_token = Token.objects.get(user=self)
            api_token.delete()
        except Exception as e:
            print(f'Could not find API token for user {self}')
            print(e)

        super().delete(*args, **kwargs)

    def make_active(self):
        self.is_active = True
        self.save()

    def gen_api_token(self):
        try:
            return Token.objects.get(user=self)
        except Exception as e:
            print(e)
            return Token.objects.create(user=self)



    def __str__(self):
        return self.email