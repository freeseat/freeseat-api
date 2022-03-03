from apps.articles.serializers import ArticleSerializer
from packages.restframework.pagination import PageNumberPaginationWithPageCounter
from rest_framework import viewsets

__all__ = ["ArticlesAPIViewSet"]


class ArticlesAPIViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = PageNumberPaginationWithPageCounter
    serializer_class = ArticleSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
