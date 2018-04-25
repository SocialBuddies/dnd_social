from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _

from utils.cleaning import normalise_email

User = get_user_model()


class LoginForm(forms.Form):
    """create login form with placeholders for fields"""

    email = forms.CharField(required=True, label="Email")
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if password and email:
            user = authenticate(email=normalise_email(email), password=password)
            if not user:
                raise forms.ValidationError("Login invalid")
        return self.cleaned_data

    def login(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user


class RegistrationForm(forms.Form):
    """ User Registration form """

    username = forms.CharField(max_length=30, required=True)
    email = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, label="Confirm password", widget=forms.PasswordInput())

    def clean_username(self):
        """
        Validate for usernames, keep upper/lowercase but compare without them
        """
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username__iexact=username)
            raise forms.ValidationError(_("This username already exists"))
        except User.DoesNotExist:
            return username

    def clean_email(self):
        """
        Validates that the email address does not exist already, and tests
        against lower cased email address.
        """
        raw_email = self.cleaned_data.get('email')
        email = normalise_email(raw_email)
        try:
            User.objects.get(email__iexact=email)
            raise forms.ValidationError(_("This email already exists"))
        except User.DoesNotExist:
            return email

    def clean(self):
        # validate passwords
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")

        return self.cleaned_data

    def save(self):
        # remove password2
        self.cleaned_data.pop('password2')
        return User.objects.create_user(**self.cleaned_data)
