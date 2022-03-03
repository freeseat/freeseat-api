from django.db import models
from django.utils import timezone

__all__ = ["PhoneNumberField", "get_file_directory"]


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
