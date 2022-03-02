from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

__all__ = ["CreatedByUserAdminMixin"]


class CreatedByUserAdminMixin:
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if hasattr(instance, "created_at") and not instance.created_at:
                instance.created_by = request.user
            instance.save()
        formset.save_m2m()

    @admin.display(description=_("created by"))
    def link_to_created_by(self, obj):
        link = reverse("admin:accounts_user_change", args=[obj.created_by_id])
        return format_html('<a href="%s">%s</a>' % (link, obj.created_by))
