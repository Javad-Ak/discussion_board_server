from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager as BasicUserManager, PermissionsMixin, AbstractUser

from django.core.exceptions import ValidationError
from django.db import models
import uuid


def validate_avatar(value):
    if value and value.size > 2000000:
        raise ValidationError("Avatar image must be up to 2MB.")


class UserManager(BasicUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """ Create and save a custom user with the given username and password. """
        if not username:
            raise ValueError('you must provide a username.')

        if extra_fields.get('is_superuser') is False:
            if not extra_fields['email']:
                raise ValueError('you must provide an email.')

            if not extra_fields.get('first_name'):
                raise ValueError('you must provide a first name.')

            if not extra_fields.get('last_name'):
                raise ValueError('you must provide a last name.')

        if email := extra_fields.get('email'):
            extra_fields['email'] = self.normalize_email(email)

        user = super().create_user(username=username, password=password, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """ Create and save a custom SuperUser with the given username and password. """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is False:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is False:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username=username, password=password, **extra_fields)


class User(AbstractUser):
    """ Custom user model with additional fields """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    avatar = models.ImageField(validators=[validate_avatar], upload_to='avatars/', blank=True)
    bio = models.TextField(blank=True)

    # settings
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
