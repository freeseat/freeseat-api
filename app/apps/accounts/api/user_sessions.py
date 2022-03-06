from apps.accounts.serializers import UserSessionSerializer
from apps.accounts.services import UserSessionService
from rest_framework import generics, status
from rest_framework.response import Response

__all__ = ["UserSessionCreateAPIView"]


class UserSessionCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSessionSerializer
    model = serializer_class.Meta.model

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            user_session = self.model.objects.get(id=serializer.data.get("id"))
            UserSessionService.update_last_active_time(user_session)
            raise e

        self.perform_create(serializer)

        user_session = serializer.instance
        UserSessionService.update_last_active_time(user_session)

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
