from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = ["AbstractUUIDModel"]


class AbstractUUIDModel(models.Model):
    id = models.UUIDField(
        verbose_name=_("id"),
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    class Meta:
        abstract = True
