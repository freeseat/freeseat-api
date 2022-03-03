import simple_history
from apps.articles.models import Article
from modeltranslation.translator import TranslationOptions, register

__all__ = ["ArticleTranslationOptions"]


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "content",
    )


simple_history.register(Article)
