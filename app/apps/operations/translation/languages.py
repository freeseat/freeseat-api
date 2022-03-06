import simple_history
from apps.operations.models import Language
from modeltranslation.translator import TranslationOptions, register

__all__ = ["LanguageTranslationOptions"]


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ("name",)


simple_history.register(Language)
