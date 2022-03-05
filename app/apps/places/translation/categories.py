import simple_history
from apps.places.models import POICategory
from modeltranslation.translator import TranslationOptions, register

__all__ = ["POICategoryTranslationOptions"]


@register(POICategory)
class POICategoryTranslationOptions(TranslationOptions):
    fields = ("name", "description")


simple_history.register(POICategory, inherit=True)
