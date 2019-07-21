import jwt
import random
import string
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, UserManager
)
from django.conf import settings
from datetime import datetime, timedelta


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, **kwargs):
        """Create and return a `User` with an email, username and password."""
        
        user = User(email=self.normalize_email(kwargs['email']), name=kwargs['name'],\
                city=kwargs['city'])
        user.set_password(kwargs['password'])
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):

    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255)
    # access_token = models.CharField(max_length=255, null=False)
    refresh_token = models.CharField(max_length=255, null=False)
    first_time_login = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):

        return self.email


    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(minutes=2)
        token = jwt.encode({
            'id': self.id,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    def generate_refresh_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        token = jwt.encode({
            'id': self.id,
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    def get_user(self, user_id):

        user = User.objects.filter(id=user_id, is_active=True).first()
        if not user:
            raise ValidationError(response['error']['user_exist'])
        return user
