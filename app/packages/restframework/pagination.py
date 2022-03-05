from collections import OrderedDict

from rest_framework import pagination
from rest_framework.response import Response

__all__ = ["PageNumberPaginationWithPageCounter"]


class PageNumberPaginationWithPageCounter(pagination.PageNumberPagination):
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("total_pages", self.page.paginator.num_pages),
                    ("results", data),
                ]
            )
        )

    def paginate_queryset(self, queryset, request, view=None):
        if request.query_params.get("disable_pagination") == "true":
            return None
        return super().paginate_queryset(queryset, request, view)
