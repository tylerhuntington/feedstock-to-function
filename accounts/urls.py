"""
By default, django.contrib.auth includes these views:

accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']

"""
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from accounts import forms
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            authentication_form=forms.CustomUserAuthenticationForm
        ),
    ),
    path(
        'create/',
        views.CreateAccountView.as_view(),
        name="create_account"
    ),
    path(
        'confirm/',
        views.ConfirmAccountRequestedView.as_view(),
        name="confirm_account_requested"
    ),
    path(
        'confirm_email/<uidb64>/<token>/',
        views.ConfirmEmailView.as_view(),
        name="confirm_email"
    ),
    path(
        'change/',
        views.ChangeAccountView.as_view(),
        name="change"
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.CustomPasswordResetConfirmView.as_view(
            form_class=forms.CustomUserPasswordSetForm
        ),
        name="password_reset_confirm"
    ),
    path(
        'reset/done',
        views.CustomPasswordResetCompleteView.as_view(),
        name="custom_password_reset_done"
    ),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            form_class=forms.CustomUserPasswordResetForm
        ),
        name="password_reset"
    ),
    path(
        'inactive/',
        views.AccountInactiveView.as_view(
        ),
        name="inactive"
    ),
    # path(
    #     'login_with_google/',
    #     views.LoginWithGoogleView.as_view(),
    #     name="login_with_google"
    # ),
    # path(
    #     'login_with_google/callback/',
    #     auth_views.LoginWithGoogleViewCallback.as_view(),
    #     name="login_with_google_callback"
    # ),
    path(
        'activate/<uidb64>/<token>/',
        views.ActivateAccountView.as_view(),
    ),
    re_path(
        'resend/(?P<uidb64>[0-9A-Za-z_\-]+)/$',
        views.ResendEmailConfirmationLinkView.as_view(),
        name="resend_token"
    ),
]
