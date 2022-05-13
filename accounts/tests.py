from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.http import HttpResponse


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)

class AccountsViewsTests(TestCase):

    def setUp(self):
        self.new_user_email = 'user@example.org'

    def test_create_account_view(self):
        rv = self.client.get(reverse('accounts:create_account'))
        self.assertTrue(isinstance(rv, HttpResponse))
        self.assertEqual(rv.status_code, 200)
        self.assertTrue('Create New Account' in str(rv.content))

    def test_confirm_account_requested_view(self):
        session = self.client.session
        session['new_user_email'] = self.new_user_email
        session.save()
        rv = self.client.get(reverse('accounts:confirm_account_requested'))
        self.assertTrue(isinstance(rv, HttpResponse))
        self.assertEqual(rv.status_code, 200)
        self.assertTrue('Thanks for Registering' in str(rv.content))
        self.assertTrue(self.new_user_email in str(rv.content))

    def test_confirm_account_requested_view(self):
        session = self.client.session
        session['new_user_email'] = self.new_user_email
        session.save()
        rv = self.client.get(reverse('accounts:confirm_account_requested'))
        self.assertTrue(isinstance(rv, HttpResponse))
        self.assertEqual(rv.status_code, 200)
        self.assertTrue('Thanks for Registering' in str(rv.content))
        self.assertTrue(self.new_user_email in str(rv.content))

