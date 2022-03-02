from uuid import uuid4

from django.db import models
from django.utils import timezone

__all__ = ["UUID4Field", "LowerCaseCharField", "PhoneNumberField", "get_file_directory"]


class UUID4Field(
    models.fields.AutoFieldMixin,
    models.UUIDField,
    metaclass=models.fields.AutoFieldMeta,
):
    def __init__(self, verbose_name=None, **kwargs):
        kwargs["default"] = uuid4()
        super().__init__(verbose_name, **kwargs)


class LowerCaseCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(LowerCaseCharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class PhoneNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        if not kwargs.get("max_length"):
            kwargs["max_length"] = 16
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if not value:
            return None
        return "+" + "".join([x for x in value if x.isdigit()])


def get_file_directory(instance, filename):
    return (
        f"{instance.__class__.__name__.lower()}s/{instance.id}/"
        f"{timezone.now().strftime('%Y-%m-%d_%H-%M-%S')}/{filename}"
    )
