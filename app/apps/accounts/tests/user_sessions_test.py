from django.urls import reverse
from pytest_django.asserts import assertNumQueries


class TestUserSessionsCreate:
    url = reverse("accounts:user-sessions-list")

    def test_user_session_creation_is_available_for_unauthenticated_users(
        self,
        api_client,
    ):
        # Given
        user_session_id = "1234567890"
        data = {
            "id": user_session_id,
        }

        # When
        with assertNumQueries(2):
            response = api_client.post(self.url, data=data)

        # Then
        assert response.status_code == 201
        assert response.json() == data

    def test_user_session_creation_with_duplicated_id_fails(
        self, api_client, user_session
    ):
        # Given
        user_session_id = "1234567890"

        user_session(id=user_session_id)

        data = {
            "id": user_session_id,
        }

        # When
        with assertNumQueries(1):
            response = api_client.post(self.url, data=data)

        # Then
        assert response.status_code == 400
