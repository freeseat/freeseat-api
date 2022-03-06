from apps.accounts.models import UserSession
from apps.accounts.serializers import UserSessionSerializer
from apps.accounts.services import UserSessionService
from rest_framework import generics, status
from rest_framework.response import Response

__all__ = ["UserSessionCreateAPIView"]


class UserSessionCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSessionSerializer
    model = UserSession

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        _, created = UserSessionService.get_or_create_user_session(**serializer.data)

        headers = self.get_success_headers(serializer.data)

        if created:
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK

        return Response(serializer.data, status=status_code, headers=headers)
