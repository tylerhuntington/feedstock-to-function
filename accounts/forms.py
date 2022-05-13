from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, _unicode_ci_compare
)
from django.contrib.auth.forms import (
    AuthenticationForm, SetPasswordForm, PasswordResetForm
)
from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field, HTML, Button, Div


from .models import CustomUser
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
UserModel = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'placeholder': 'Password'
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'placeholder': 'Confirm Password'
            }
        ),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    eula_accepted = forms.BooleanField(
        label=_(
            'I am not a robot'
        ),
        required=True,
        widget=forms.CheckboxInput()
    )


    class Meta(UserCreationForm):
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'email', 'affiliation', 'field_of_work'
        )
        field_order = [
            'first_name', 'last_name', 'email', 'affiliation', 'field_of_work'
        ]
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'First Name',
                    'autofocus': True
                }
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Last Name'}
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Email Address',
                    'autofocus': False
                }
            ),
            'affiliation': forms.TextInput(
                attrs={'placeholder': 'Organization/Company'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'create-account-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))
        self.helper.form_class = 'form-group'
        self.helper.form_show_labels = True
        labeled_fields = ['eula_accepted']
        for field in self.fields.keys():
            if field not in labeled_fields:
                self.fields[field].label = False

class CustomUserChangeForm(UserChangeForm):
    password = None
    dummy_password = forms.CharField(
        label=_("Password"),
        strip=False,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '***********',
                'readonly': True,
            }
        ),
    )

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('email', 'affiliation', 'field_of_work')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-user-change-form'
        self.helper.form_method = 'post'
        self.helper.add_input(
            Button(
                'password reset button',
                'Reset Password',
                css_class='btn-warning',
                css_id='pwd-reset-btn',
                onclick="javascript:window.location.href = '../password_reset'",
            )
        )
        self.helper.add_input(
            Submit(
                'save-changes-btn', 'Save Changes', css_id='save-changes-btn'
            )
        )
        self.helper.form_class = 'form-group'
        self.helper.form_show_labels = True


class CustomUserAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(
            attrs={'autofocus': True, 'placeholder': 'Email'}
        )
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'placeholder': 'Password',
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-auth-form'
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit(
                'submit',
                'Sign in',
                css_class='btn-success'
            )
        )

        self.helper.form_class = 'form-group'
        self.helper.form_style = 'inline'
        self.helper.form_show_labels = False


class CustomUserPasswordResetForm(PasswordResetForm):

    email = forms.CharField(
        label=_("Email Address:"),
        required=True
    )

    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta:
        model = CustomUser
        fields = ('email',)

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % email_field_name: email,
            'is_active': True,
        })
        return (u for u in active_users)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-auth-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send Reset Link'))
        self.helper.form_class = 'form-group'


class CustomUserPasswordSetForm(SetPasswordForm):

    class Meta:
        model = CustomUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-auth-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.form_class = 'form-group'






