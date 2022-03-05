from django.db import models
from django.utils.translation import gettext_lazy as _
from packages.django.db.models import AbstractUUIDModel
from treebeard.mp_tree import MP_Node

__all__ = ["PlaceCategory"]


class PlaceCategory(AbstractUUIDModel, MP_Node):
    created_at = models.DateTimeField(
        verbose_name=_("created at"), auto_now_add=True, editable=False, db_index=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"), auto_now=True, editable=False, db_index=True
    )

    created_by = models.ForeignKey(
        verbose_name=_("created by"),
        to="accounts.User",
        on_delete=models.PROTECT,
        related_name="+",
        editable=False,
        db_index=True,
        null=True,
    )

    name = models.CharField(verbose_name=_("name"), max_length=255, db_index=True)
    description = models.TextField(
        verbose_name=_("description"), default="", blank=True
    )
    is_active = models.BooleanField(
        verbose_name=_("active"), default=True, db_index=True
    )

    node_order_by = ["name"]

    class Meta:
        verbose_name = _("place category")
        verbose_name_plural = _("place categories")

    def __str__(self):
        return self.name
