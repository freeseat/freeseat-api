from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from packages.django.db import PhoneNumberField

__all__ = ["User"]


class User(AbstractUser):
    id = models.UUIDField(
        verbose_name=_("id"),
        default=uuid4,
        primary_key=True,
        editable=False,
    )

    password = models.CharField(_("password"), max_length=128)
    username = models.CharField(
        verbose_name=_("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        db_index=True,
    )
    first_name = models.CharField(
        verbose_name=_("first name"), max_length=150, blank=True, db_index=True
    )
    last_name = models.CharField(
        verbose_name=_("last name"), max_length=150, blank=True, db_index=True
    )
    email = models.EmailField(
        verbose_name=_("email address"),
        unique=True,
        db_index=True,
        null=True,
        blank=True,
    )
    phone_number = PhoneNumberField(
        verbose_name=_("phone number"),
        unique=True,
        null=True,
        blank=True,
        db_index=True,
    )

    last_login = models.DateTimeField(
        verbose_name=_("last login"),
        blank=True,
        null=True,
        editable=False,
        db_index=True,
    )
    date_joined = models.DateTimeField(
        verbose_name=_("date joined"),
        auto_now_add=True,
        editable=False,
        db_index=True,
    )

    is_staff = models.BooleanField(
        verbose_name=_("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
        db_index=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
        db_index=True,
    )
    is_superuser = models.BooleanField(
        verbose_name=_("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
        db_index=True,
    )

    class RegistrationSource(models.TextChoices):
        CONSOLE = "console", _("console")
        ADMIN_PANEL = "admin_panel", _("admin panel")

    registration_source = models.CharField(
        verbose_name=_("registration source"),
        max_length=32,
        choices=RegistrationSource.choices,
        default=RegistrationSource.CONSOLE,
        editable=False,
        db_index=True,
    )

    @property
    def full_name(self) -> str:
        return self.get_full_name()

    class Meta:
        ordering = ("-date_joined",)
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = None
        super().save(*args, **kwargs)
