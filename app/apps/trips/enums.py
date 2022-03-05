from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = ["LuggageSize", "TripState"]


class LuggageSize(models.IntegerChoices):
    SMALL_BAGS = 1, _("small bags")
    LARGE_BAGS = 2, _("large bags")
    CARGO = 3, _("cargo")


class TripState(models.TextChoices):
    ACTIVE = "active", _("active")
    CANCELLED = "cancelled", _("cancelled")
    COMPLETED = "completed", _("completed")
    OUTDATED = "outdated", _("outdated")
    INVALID = "invalid", _("invalid")
