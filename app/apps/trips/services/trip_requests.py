from apps.accounts.models import Language
from apps.comments.models import Comment
from apps.logs.models import TripRequestSearchLog
from apps.trips.enums import TripState
from apps.trips.models import Trip, TripRequest, TripRequestReport, WayPoint
from django.db import transaction
from django.utils import timezone

__all__ = ["TripRequestService"]


class TripRequestService:
    @classmethod
    @transaction.atomic
    def request_trip(cls, data: dict) -> TripRequest:
        trip_data = data.pop("trip")
        waypoints = trip_data.pop("waypoints")
        spoken_languages = data.pop("spoken_languages")

        active_for = data.pop("active_for", 24 * 60 * 60)

        active_until = timezone.now() + timezone.timedelta(seconds=active_for)

        trip = Trip.objects.create(**trip_data)

        for waypoint in waypoints:
            WayPoint.objects.create(
                trip=trip,
                order=waypoint.get("order"),
                point=waypoint.get("point"),
            )

        data["trip"] = trip
        data["starting_point"] = trip.waypoints.first().point

        trip_request = TripRequest.objects.create(active_until=active_until, **data)
        trip_request.spoken_languages.set(spoken_languages)

        return trip_request

    @classmethod
    @transaction.atomic
    def update_requested_trip(
        cls, trip_request: TripRequest, data: dict
    ) -> TripRequest:
        trip_data = data.pop("trip")
        waypoints = trip_data.pop("waypoints")
        spoken_languages = data.pop("spoken_languages")

        active_for = data.pop("active_for", 24 * 60 * 60)

        active_until = timezone.now() + timezone.timedelta(seconds=active_for)

        trip = trip_request.trip

        Trip.objects.filter(id=trip.id).update(**trip_data)

        trip.waypoints.all().delete()

        for waypoint in waypoints:
            WayPoint.objects.create(
                trip=trip,
                order=waypoint.get("order"),
                point=waypoint.get("point"),
            )

        data["starting_point"] = trip.waypoints.first().point

        TripRequest.objects.filter(id=trip_request.id).update(active_until=active_until, **data)
        trip_request.spoken_languages.set(spoken_languages)

        trip_request.refresh_from_db()

        return trip_request

    @classmethod
    @transaction.atomic
    def _change_trip_request_state(
        cls,
        trip_request: TripRequest,
        to_state: TripState,
        comment: str,
        report: dict,
    ) -> TripRequest:
        trip_request.state = to_state
        trip_request.save(update_fields=["state"])

        if comment:
            Comment.objects.create(content=comment, content_object=trip_request)

        if report:
            TripRequestReport.objects.create(trip_request=trip_request, **report)

        return trip_request

    @classmethod
    def cancel_requested_trip(
        cls, trip_request: TripRequest, data: dict
    ) -> TripRequest:
        return cls._change_trip_request_state(
            trip_request,
            TripState.CANCELLED,
            data.get("comment"),
            data.get("report"),
        )

    @classmethod
    def complete_requested_trip(
        cls, trip_request: TripRequest, data: dict
    ) -> TripRequest:
        return cls._change_trip_request_state(
            trip_request,
            TripState.COMPLETED,
            data.get("comment"),
            data.get(
                "report",
            ),
        )

    @classmethod
    def extend_trip_request(
        cls,
        trip_request: TripRequest,
        extend_for: int,
    ) -> TripRequest:

        if trip_request.active_for:
            trip_request.active_until = trip_request.active_until + timezone.timedelta(
                seconds=extend_for
            )
        else:
            trip_request.active_until = timezone.now() + timezone.timedelta(
                seconds=extend_for
            )

        trip_request.save(update_fields=["active_until", "updated_at"])
        return trip_request

    @classmethod
    def log_trip_request_search(
        cls,
        user_session=None,
        point=None,
        area=None,
        radius=None,
        number_of_people=None,
        with_pets=None,
        luggage_size=None,
        spoken_languages=None,
        results=None,
    ):
        if with_pets == "true":
            with_pets = True
        elif with_pets == "false":
            with_pets = False
        elif with_pets == "unknown":
            with_pets = None

        if not user_session:
            user_session = None

        if not number_of_people:
            number_of_people = None

        if not luggage_size:
            luggage_size = None

        try:
            trip_request_search_log = TripRequestSearchLog.objects.create(
                user_session_id=user_session,
                point=point,
                radius=radius,
                area=area,
                number_of_people=number_of_people,
                with_pets=with_pets,
                luggage_size=luggage_size,
                number_of_results=results.count(),
            )

            if spoken_languages:
                spoken_languages = spoken_languages.split(",")
                languages = Language.objects.filter(code__in=spoken_languages)
                trip_request_search_log.spoken_languages.set(languages)

            if results:
                trip_request_search_log.results.set(results)

        except ValueError:
            pass
