from apps.articles.models import Article
from rest_framework import serializers

__all__ = ["ArticleSerializer"]


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "created_at",
            "name",
            "content",
        ]
