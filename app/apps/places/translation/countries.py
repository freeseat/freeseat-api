import simple_history
from apps.places.models import Country
from modeltranslation.translator import TranslationOptions, register

__all__ = ["CountryTranslationOptions"]


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ("name",)


simple_history.register(Country, inherit=True)
