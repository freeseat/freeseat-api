import simple_history
from apps.accounts.models import ContactInformation

__all__ = []


simple_history.register(ContactInformation, inherit=True)
