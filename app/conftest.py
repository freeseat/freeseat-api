import pytest
from model_bakery import baker
from rest_framework.test import APIClient


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker("django_db")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_api_client(user):
    client = APIClient()
    client.force_authenticate(user())
    return client


@pytest.fixture
def staff_api_client(staff_user):
    client = APIClient()
    client.force_authenticate(staff_user())
    return client


@pytest.fixture
def user():
    def create_user(**kwargs):
        return baker.make(
            "accounts.User",
            is_staff=False,
            is_superuser=False,
            **kwargs,
        )

    return create_user


@pytest.fixture
def staff_user():
    def create_staff_user(**kwargs):
        return baker.make(
            "accounts.User",
            is_staff=True,
            is_superuser=False,
            **kwargs,
        )

    return create_staff_user


@pytest.fixture
def language_batch():
    def create_language_batch(n=1, **kwargs):
        return baker.make(
            "accounts.Language",
            _quantity=n,
            **kwargs,
        )

    return create_language_batch


@pytest.fixture
def language():
    def create_language(**kwargs):
        return baker.make(
            "accounts.Language",
            **kwargs,
        )

    return create_language


@pytest.fixture
def user_session():
    def create_user_session(**kwargs):
        return baker.make(
            "accounts.UserSession",
            **kwargs,
        )

    return create_user_session


@pytest.fixture
def article_batch():
    def create_article_batch(n=1, **kwargs):
        return baker.make(
            "articles.Article",
            _quantity=n,
            **kwargs,
        )

    return create_article_batch
