from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

__all__ = ["CreatedByUserAdminMixin", "ContentObjectAdminMixin"]


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


class ContentObjectAdminMixin:
    content_object_field_name = "content_object"

    @admin.display(description=_("object"))
    def link_to_content_object(self, obj):
        if content_object := getattr(obj, self.content_object_field_name):
            link = reverse(
                "admin:%s_%s_change"
                % (
                    content_object._meta.app_label,
                    content_object._meta.model_name,
                ),
                args=[content_object.id],
            )
            return format_html(
                '<a href="%s">%s</a>'
                % (
                    link,
                    ": ".join(
                        [
                            content_object._meta.verbose_name.title(),
                            str(content_object),
                        ]
                    ),
                )
            )
