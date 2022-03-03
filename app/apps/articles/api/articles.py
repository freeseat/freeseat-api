from apps.articles.serializers import ArticleSerializer
from rest_framework import viewsets

__all__ = ["ArticlesAPIViewSet"]


class ArticlesAPIViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
