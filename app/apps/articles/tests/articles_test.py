from django.urls import reverse
from pytest_django.asserts import assertNumQueries


class TestArticlesList:
    url = reverse("articles:articles-list")

    def test_articles_list_is_available_for_unauthenticated_users(
        self,
        api_client,
        article_batch,
    ):
        # Given
        article_batch(30)

        # When
        with assertNumQueries(2):
            response = api_client.get(self.url)

        # Then
        assert response.status_code == 200
        assert response.json().get("count") == 30
        assert len(response.json().get("results")) == 20
        assert response.json().get("total_pages") == 2
        assert response.json().get("total_pages") == 2
        assert len(response.json().get("results")[0]) == 4
        assert "id" in response.json().get("results")[0]
        assert "name" in response.json().get("results")[0]
        assert "created_at" in response.json().get("results")[0]
        assert "content" in response.json().get("results")[0]
