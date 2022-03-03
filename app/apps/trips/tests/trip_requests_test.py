from apps.accounts.models import Language
from django.urls import reverse
from pytest_django.asserts import assertNumQueries


class TestTripRequestsCRUD:
    list_url = reverse("trips:trip-requests-list")
    # detail_url = reverse("trips:trip-requests-detail")

    def test_trip_request_creation_is_available_for_unauthenticated_user(
        self, api_client, language_batch, user_session
    ):
        # Given
        language_batch(4)
        current_user_session = user_session()
        number_of_people = 2
        with_pets = True
        luggage_size = 2
        spoken_languages = Language.objects.all().values_list("code", flat=True)[:2]
        comment = "my phone number"
        waypoints = [
            {"order": 0, "point": [4.746439964831319, 46.9112455365038]},
            {"order": 1, "point": [5.066482548136264, 46.98282884604268]},
        ]
        route_length = 0.00123

        data = {
            "user_session": current_user_session.id,
            "number_of_people": number_of_people,
            "with_pets": with_pets,
            "luggage_size": luggage_size,
            "spoken_languages": spoken_languages,
            "comment": comment,
            "waypoints": waypoints,
            "route_length": route_length,
        }

        # When
        with assertNumQueries(16):
            response = api_client.post(self.list_url, data=data, format="json")

        # Then
        assert response.status_code == 201
        assert len(response.json()) == 9
        assert "id" in response.json()
        assert "last_active_at" in response.json()
        assert response.json().get("number_of_people") == number_of_people
        assert response.json().get("with_pets") == with_pets
        assert response.json().get("luggage_size") == luggage_size
        assert response.json().get("comment") == comment
        assert response.json().get("route_length") == route_length
        assert len(response.json().get("spoken_languages")) == len(spoken_languages)
        assert response.json().get("waypoints") == waypoints
