"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/2022-03-05/operations/",
        include("apps.operations.urls", namespace="operations"),
    ),
    path(
        "api/2022-03-05/accounts/", include("apps.accounts.urls", namespace="accounts")
    ),
    path(
        "api/2022-03-05/articles/", include("apps.articles.urls", namespace="articles")
    ),
    path("api/2022-03-05/trips/", include("apps.trips.urls", namespace="trips")),
    path("api/2022-03-05/places/", include("apps.places.urls", namespace="places")),
    path("api/2022-03-05/docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/2022-03-05/docs/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/2022-03-05/docs/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
