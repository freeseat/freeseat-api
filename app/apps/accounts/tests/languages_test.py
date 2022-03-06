# TODO: drop file
from django.urls import reverse
from pytest_django.asserts import assertNumQueries


class TestLanguagesList:
    url = reverse("accounts:languages-list")

    def test_list_of_languages_is_public_available(self, api_client, language_batch):
        # Given
        language_batch(10)

        # When
        with assertNumQueries(1):
            response = api_client.get(self.url)

        # Then
        assert response.status_code == 200
        assert len(response.json()) == 10
        assert "code" in response.json()[0]
        assert "name" in response.json()[0]
        assert 2 == len(response.json()[0])
