import json
import requests
from oauthlib.oauth2 import WebApplicationClient
from django.views.generic import View
from accounts import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .models import CustomUser
from django.conf import settings
from django.urls import reverse_lazy, reverse

from allauth.account.signals import user_signed_up, email_confirmed
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    new_user_redir_url = '/accounts/confirm/'

    user.is_active = False
    user.save()
    send_email_address_confirm_email_to_new_user(user)
    return HttpResponseRedirect(new_user_redir_url)


class FormView(View):
    form_class = None
    template_name = None
    # initial values with which to populate form
    initial = {}
    redir_url = ''

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect(self.redir_url)

        return render(request, self.template_name, {'form': form})

class InfoBoxView(View):
    template_name = None
    context = {}

    def get(self, request, *args, **kwargs):
        return render(
            request,
            context=self.context,
            template_name=self.template_name
        )


class CreateAccountView(FormView):
    form_class = forms.CustomUserCreationForm
    template_name = 'create_account.html'
    redir_url = '/accounts/confirm/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # create user object and add to DB
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # save the email address of new user to session variable
            request.session['new_user_email'] = user.email

            send_email_address_confirm_email_to_new_user(user)
            return HttpResponseRedirect(self.redir_url)

        return render(request, self.template_name, {'form': form})



class ConfirmEmailView(View):
    failure_template = 'failed_email_confirmation.html'
    success_template = 'confirm_email_success.html'

    def get(self, request, uidb64=None, token=None):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        # except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        except Exception:
            user = None
        if user is not None:
            if account_activation_token.check_token(user, token):
                send_new_user_approval_request_to_site_admin(user)
            return render(
                request, template_name=self.success_template
            )
        return render(
            request,
            template_name=self.failure_template,
            context={'uidb64': uidb64}
        )




# class LoginWithGoogleCallbackView(View):
#     redir_url = ''
#     def get(self, request, *args, **kwargs):
#         # init OAuth client for google logins
#         client = WebApplicationClient(settings['GOOGLE_CLIENT_ID'])
#         # Get authorization code Google sent back to you
#         code = request.args.get("code")
#
#         # Find out what URL to hit to get tokens that allow you to ask for
#         # things on behalf of a user
#         google_provider_cfg = LoginWithGoogleView.get_google_provider_cfg()
#         token_endpoint = google_provider_cfg["token_endpoint"]
#         token_url, headers, body = client.prepare_token_request(
#             token_endpoint,
#             authorization_response=request.url.replace('http', 'https'),
#             redirect_url=request.base_url.replace('http', 'https'),
#             code=code
#         )
#         token_response = requests.post(
#             token_url,
#             headers=headers,
#             data=body,
#             auth=(
#                 settings['GOOGLE_CLIENT_ID'],
#                 settings['GOOGLE_CLIENT_SECRET']
#             ),
#         )
#
#         # Parse the tokens
#         client.parse_request_body_response(
#             json.dumps(token_response.json()))
#
#         # Now that we have tokens, find and hit the URL
#         # from Google that gives the user's profile information,
#         # including their Google profile image and email
#         userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
#         uri, headers, body = client.add_token(userinfo_endpoint)
#         userinfo_response = requests.get(uri, headers=headers, data=body)
#
#         # maker sure user's email is verified
#         if userinfo_response.json().get("email_verified"):
#             unique_id = userinfo_response.json()["sub"]
#             users_email = userinfo_response.json()["email"]
#             picture = userinfo_response.json()["picture"]
#             users_name = userinfo_response.json()["given_name"]
#         else:
#             return "User email not available or not verified by Google.", 400
#
#         # Send user to desired endpoint
#         try:
#             user = CustomUser.objects.get(email__iexact=users_email)
#             # if user is already active, log them in
#             if user.is_active:
#                 return HttpResponseRedirect(self.redir_url)
#
#         except CustomUser.DoesNotExist:
#             user = CustomUser.objects.create(email=users_email)
#             user.is_active = False
#             # user.save()
#
#             # save the email address of new user to session variable
#             # request.session['new_user_email'] = user.email
#
#             send_email_address_confirm_email_to_new_user(user)
#             return HttpResponseRedirect(self.redir_url)
#
#
# class LoginWithGoogleView(View):
#     def get(self, request, *args, **kwargs):
#
#         # init OAuth client for google logins
#         client = WebApplicationClient(settings['GOOGLE_CLIENT_ID'])
#         # Find out what URL to hit for Google login
#         google_provider_cfg = self.get_google_provider_cfg()
#         authorization_endpoint = google_provider_cfg["authorization_endpoint"]
#
#         # Use library to construct the request for Google login and provide
#         # scopes that let you retrieve user's profile from Google
#         request_uri = client.prepare_request_uri(
#             authorization_endpoint,
#             redirect_uri=request.base_url.replace('http',
#                                                   'https') + "/callback",
#             scope=["openid", "email", "profile"],
#         )
#         return redirect(request_uri)
#
#
#     @staticmethod
#     def get_google_provider_cfg():
#         return requests.get(
#             settings['GOOGLE_DISCOVERY_URL']).json()


class ChangeAccountView(LoginRequiredMixin, FormView):
    form_class = forms.CustomUserChangeForm
    template_name = 'change_account.html'
    redir_url = '/accounts/change/'

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(email=request.user)
        initial = user.__dict__
        form = self.form_class(initial=initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.get(email=request.user)
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            context = {
                'form': form,
                'user': user,
                'request_type': 'post'
            }
            return render(
                request,
                template_name=self.template_name,
                context=context
            )
        return HttpResponse('Error: Invalid Form')

class AccountInactiveView(InfoBoxView):
    template_name = 'inactive_account.html'


class ResendEmailConfirmationLinkView(View):
    redir_url = '/accounts/confirm/'

    def get(self, request, uidb64=None, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None:
            send_email_address_confirm_email_to_new_user(user)
            # redirect to confirmation of account request infobox page
            return HttpResponseRedirect(self.redir_url)

        return HttpResponse('Error: account not found!')


class ActivateAccountView(View):
    success_template = 'confirm_account_activated.html'
    failure_template = 'failed_account_activation.html'

    def get(self, request, uidb64=None, token=None):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        # except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        except Exception:
            user = None
        if user is not None:
            if account_activation_token.check_token(user, token):
                # make the user active
                user.make_active()

                # generate API token for new user
                user.gen_api_token()

                send_account_activated_email_to_user(user)
                return render(
                    request, template_name=self.success_template
                )

        return render(
            request,
            template_name=self.failure_template,
            context={'uidb64': uidb64}
        )


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = '/accounts/reset/done/'


class CustomPasswordResetCompleteView(InfoBoxView):
    template_name = 'password_reset_complete.html'


class ConfirmAccountRequestedView(InfoBoxView):
    template_name = 'confirm_account_requested.html'


# helper functions
def send_email_address_confirm_email_to_new_user(user):
    mail_subject = 'Confirm your email address'
    message = render_to_string('account_confirmation_email.html', {
        'user': user,
        'domain': settings.SITE_DOMAIN,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    # to_email = form.cleaned_data.get('email')
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()


def send_new_user_approval_request_to_site_admin(user):
        mail_subject = 'New user account requested'
        message = render_to_string('account_request_email.html', {
            'user': user,
            'domain': settings.SITE_DOMAIN,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = settings.EMAIL_HOST_USER
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()



def send_account_activated_email_to_user(user):
    mail_subject = 'Account Approved!'
    message = render_to_string('account_activated_email.html', {
        'user': user,
        'domain': settings.SITE_DOMAIN,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    print('MESSAGE')
    print(message)
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
