import uuid

from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, username: str, password: str = None, is_staff=False, is_superuser=False):
        if not username:
            raise ValueError("user must have a username")

        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, password: str = None):
        user = self.create_user(
            username=username,
            password=password,
            is_staff=True,
        )
        user.is_superuser = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=150, unique=True, validators=[username_validator], error_messages={
        'unique': _("A user with that username already exists."),
    },
                                )
    password = models.CharField(max_length=8)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = MyUserManager()

    def __str__(self):
        return self.username


class Collection(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(verbose_name="description", max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return self.title


class Movie(models.Model):
    uuid = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(verbose_name="description", null=True, blank=True)
    genres = models.CharField(verbose_name="genres", max_length=255, null=True, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='collection')

    def __str__(self):
        return self.title
