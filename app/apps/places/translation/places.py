import simple_history
from apps.places.models import Place
from modeltranslation.translator import TranslationOptions, register

__all__ = ["PlaceTranslationOptions"]


@register(Place)
class PlaceTranslationOptions(TranslationOptions):
    fields = ("name", "description")


simple_history.register(Place, inherit=True)
