from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager as BasicUserManager
import re

from django.core.exceptions import ValidationError
from django.db import models
import uuid

from discussion_board import settings

DEFAULT_AVATAR = settings.STATIC_ROOT / 'avatars' / 'default_avatar.png'


def validatePhone(value):
    if value and not re.match(r'^(\+98|0)?9\d{9}$', value):
        raise ValidationError("Phone number must be entered in the format: '+98----------' or '09---------'.")


def validateAvatar(value):
    if value and value.size > 1000000:
        raise ValidationError("Avatar image must be up to 1MB.")


class UserManager(BasicUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """ Create and save a custom user with the given username and password. """
        if not username:
            raise ValueError('you must provide a username.')

        if extra_fields['is_superuser'] is False:
            if not extra_fields['email']:
                raise ValueError('you must provide an email.')

            if not extra_fields['first_name']:
                raise ValueError('you must provide a first name.')

            if not extra_fields['last_name']:
                raise ValueError('you must provide a last name.')

        extra_fields['email'] = self.normalize_email(extra_fields['email'])
        user = super().create_user(self, username, password=password, **extra_fields)
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

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    """ Custom user model """
    # basis
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(unique=True, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)

    # additional
    phone_number = models.CharField(validators=[validatePhone], max_length=32, blank=True)
    avatar = models.ImageField(validators=[validateAvatar], upload_to='avatars/', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    # settings
    objects = UserManager
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.profile = DEFAULT_AVATAR
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)
