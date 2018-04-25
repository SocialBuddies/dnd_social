from users.models import User

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import get_object_or_404
from utils.cleaning import normalise_email

User = get_user_model()


class AuthenticationBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, *args, **kwargs):
        if email is None:
            if 'username' not in kwargs or kwargs['username'] is None:
                return None
            clean_email = normalise_email(kwargs['username'])
        else:
            clean_email = normalise_email(email)

        # Check if we're dealing with an email address
        if '@' not in clean_email:
            return None
        try:
            user = User.objects.get(email=clean_email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
