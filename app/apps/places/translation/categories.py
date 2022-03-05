import simple_history
from apps.places.models import PlaceCategory
from modeltranslation.translator import TranslationOptions, register

__all__ = ["PlaceCategoryTranslationOptions"]


@register(PlaceCategory)
class PlaceCategoryTranslationOptions(TranslationOptions):
    fields = ("name", "description")


simple_history.register(PlaceCategory, inherit=True)
