import simple_history
from apps.places.models import PointOfInterest
from modeltranslation.translator import TranslationOptions, register

__all__ = ["PointOfInterestTranslationOptions"]


@register(PointOfInterest)
class PointOfInterestTranslationOptions(TranslationOptions):
    fields = ("name", "description")


simple_history.register(PointOfInterest, inherit=True)
