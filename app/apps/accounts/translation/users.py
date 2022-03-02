import simple_history
from apps.accounts.models import User

__all__ = []


simple_history.register(User, inherit=True)
