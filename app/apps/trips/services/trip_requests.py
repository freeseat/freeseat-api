from apps.accounts.models import Language
from apps.trips.enums import TripState
from apps.trips.models import Trip, TripRequest, TripRequestSearchLog, WayPoint
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

        trip = Trip.objects.create(**trip_data)

        for waypoint in waypoints:
            WayPoint.objects.create(
                trip=trip,
                order=waypoint.get("order"),
                point=waypoint.get("point"),
            )

        data["trip"] = trip
        data["starting_point"] = trip.waypoints.first().point

        trip_request = TripRequest.objects.create(**data)
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

        TripRequest.objects.filter(id=trip_request.id).update(**data)
        trip_request.spoken_languages.set(spoken_languages)

        trip_request.refresh_from_db()

        return trip_request

    @classmethod
    @transaction.atomic
    def actualize_trip_requests_list(cls, trip_requests: TripRequest.objects):
        now = timezone.now()
        trip_requests.update(last_active_at=now)

    @classmethod
    def _change_trip_request_state(
        cls, trip_request: TripRequest, to_state: TripState
    ) -> TripRequest:
        trip_request.state = to_state
        trip_request.save(update_fields=["state"])

        return trip_request

    @classmethod
    def cancel_requested_trip(cls, trip_request: TripRequest) -> TripRequest:
        return cls._change_trip_request_state(trip_request, TripState.CANCELLED)

    @classmethod
    def complete_requested_trip(cls, trip_request: TripRequest) -> TripRequest:
        return cls._change_trip_request_state(trip_request, TripState.COMPLETED)

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

        except ValueError as e:
            pass
