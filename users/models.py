# Imports
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField


# Django base user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("user_name", email.split("@")[0])
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


# Models


class User(AbstractUser):
    slug = AutoSlugField(
        populate_from="user_name",
        unique=True,
    )
    email = models.EmailField(_("email address"), unique=True)
    profile_image = models.ImageField(_("Profile Image"), null=True, blank=True)
    objects = CustomUserManager()
    user_name = models.CharField(_("User Name"), max_length=50, unique=True)
    USERNAME_FIELD = "email"
    username = None
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"


class NewsLetter(models.Model):
    email = models.EmailField(_("Email"), max_length=254)

    def __str__(self):
        return f"{self.email}"
