from django.db.models import Q
from django.utils import timezone

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Permission,
    PermissionsMixin,
)
from django.utils.translation import pgettext_lazy
from phone_field import PhoneField

from versatileimagefield.fields import VersatileImageField

from django.db import models


class UserManager(BaseUserManager):
    def create_user(
            self, email, password=None, is_staff=False, is_active=True, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        email = UserManager.normalize_email(email)
        # Google OAuth2 backend send unnecessary username field
        extra_fields.pop("username", None)

        user = self.model(
            email=email, is_active=is_active, is_staff=is_staff, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )

    def customers(self):
        return self.get_queryset().filter(
            Q(is_staff=False) | (Q(is_staff=True) & Q(orders__isnull=False))
        )

    def staff(self):
        return self.get_queryset().filter(is_staff=True)


class User(PermissionsMixin, AbstractBaseUser):
    # TODO add validator for .edu emails
    email = models.EmailField(unique=True)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    has_kid = models.BooleanField(default=False)

    # Meta inf
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True, max_length=200)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    avatar = VersatileImageField(upload_to="user-avatars", blank=True, null=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        permissions = (
            (
                "manage_users",
                pgettext_lazy("Permission description", "Manage customers."),
            ),
            ("manage_staff", pgettext_lazy("Permission description", "Manage staff.")),
            (
                "impersonate_users",
                pgettext_lazy("Permission description", "Impersonate customers."),
            ),
        )

    def get_full_name(self):
        if self.first_name or self.last_name:
            return ("%s %s" % (self.first_name, self.last_name)).strip()
        return self.email

    def get_short_name(self):
        return self.email
