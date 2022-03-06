from apps.accounts.models import UserSession
from django.utils import timezone

__all__ = ["UserSessionService"]


class UserSessionService:
    @classmethod
    def _update_last_active_time(cls, user_session: UserSession):
        user_session.last_active_at = timezone.now()
        user_session.save(update_fields=["last_active_at"])

    @classmethod
    def get_or_create_user_session(cls, id: str):
        user_session, created = UserSession.objects.get_or_create(id=id)
        cls._update_last_active_time(user_session)
        return user_session, created
