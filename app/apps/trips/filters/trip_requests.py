from apps.accounts.models import UserSession
from apps.trips.models import TripRequest
from django.utils.translation import gettext_lazy as _
from django_filters import fields, filters, filterset

__all__ = ["TripRequestFilter"]


class TripRequestFilter(filterset.FilterSet):
    user_session = filters.ModelChoiceFilter(
        method="filter_by_user_session",
        label=_("user session"),
        queryset=UserSession.objects.all(),
    )

    def filter_by_user_session(self, queryset, name, value):
        """Filtering is happening in APIViewSet's get_queryset method."""
        return queryset

    spoken_languages = filters.BaseCSVFilter(
        method="filter_by_spoken_languages",
        label=_("spoken languages"),
        widget=fields.CSVWidget,
    )

    def filter_by_spoken_languages(self, queryset, name, value):
        return queryset.filter(spoken_languages__code__in=value).distinct()

    with_pets = filters.BooleanFilter(
        method="filter_by_pets",
        label=_("with pets"),
    )

    def filter_by_pets(self, queryset, name, value):
        if value:
            return queryset
        return queryset.exclude(with_pets=True)

    number_of_people = filters.NumberFilter(
        label=_("number of people"),
        lookup_expr="lte",
    )

    luggage_size = filters.NumberFilter(
        label=_("luggage size"),
        method="filter_by_luggage_size",
    )

    def filter_by_luggage_size(self, queryset, name, value):
        if value == self.Meta.model.LuggageSize.CARGO:
            return queryset.filter(luggage_size=value)
        return queryset.filter(luggage_size__lte=value)

    lon = filters.NumberFilter(
        label=_("longitude"),
        method="filter_by_lon",
    )

    def filter_by_lon(self, queryset, name, value):
        """Filtering is happening in APIViewSet's get_queryset method."""
        return queryset

    lat = filters.NumberFilter(
        label=_("latitude"),
        method="filter_by_lat",
    )

    def filter_by_lat(self, queryset, name, value):
        """Filtering is happening in APIViewSet's get_queryset method."""
        return queryset

    radius = filters.NumberFilter(
        label=_("radius"),
        method="filter_by_radius",
    )

    def filter_by_radius(self, queryset, name, value):
        """Filtering is happening in APIViewSet's get_queryset method."""
        return queryset

    page_size = filters.NumberFilter(
        label=_("page size"),
        method="filter_by_page_size",
    )

    def filter_by_page_size(self, queryset, name, value):
        """Filtering is happening in PageNumberPaginationWithPageCounter class."""
        return queryset

    class Meta:
        model = TripRequest
        fields = [
            "user_session",
            "spoken_languages",
            "with_pets",
            "number_of_people",
            "with_pets",
            "luggage_size",
            "lon",
            "lat",
            "radius",
        ]
