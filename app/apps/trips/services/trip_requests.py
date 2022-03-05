from apps.trips.models import Trip, TripRequest, WayPoint
from django.db import transaction

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
    def _change_trip_request_state(
        cls, trip_request: TripRequest, to_state: TripRequest.TripRequestState
    ) -> TripRequest:
        trip_request.state = to_state
        trip_request.save(update_fields=["state"])

        return trip_request

    @classmethod
    def cancel_requested_trip(cls, trip_request: TripRequest) -> TripRequest:
        return cls._change_trip_request_state(
            trip_request, TripRequest.TripRequestState.CANCELLED
        )

    @classmethod
    def complete_requested_trip(cls, trip_request: TripRequest) -> TripRequest:
        return cls._change_trip_request_state(
            trip_request, TripRequest.TripRequestState.COMPLETED
        )
