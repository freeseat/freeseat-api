from django.db import models
from django.utils.translation import gettext_lazy as _
from packages.django.db.fields import PhoneNumberField
from packages.django.db.models import AbstractUUIDModel

__all__ = ["ContactInformation"]


class ContactInformation(AbstractUUIDModel):
    first_name = models.CharField(
        verbose_name=_("first name"), max_length=64, db_index=True
    )
    last_name = models.CharField(
        verbose_name=_("last name"), max_length=64, db_index=True
    )
    phone_number = PhoneNumberField(verbose_name=_("phone number"), db_index=True)
    email = models.EmailField(
        verbose_name=_("email"), default="", blank=True, db_index=True
    )

    class Meta:
        verbose_name = _("contact information")
        verbose_name_plural = _("contact information")
