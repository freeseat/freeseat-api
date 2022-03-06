from apps.accounts.models import UserSession
from django.utils import timezone

__all__ = ["UserSessionService"]


class UserSessionService:
    @classmethod
    def update_last_active_time(cls, user_session: UserSession):
        user_session.last_active_at = timezone.now()
        user_session.save(update_fields=["last_active_at"])
