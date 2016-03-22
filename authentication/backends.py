from django.conf import settings
from django.contrib.auth.hashers import check_password
from authentication.models import Account

class EmailAuthBackend(object):
    """
    A custom authentication backend. Allows users to log in using their email address.
    """

    def authenticate(self, email=None, password=None):
        """
        Authentication method
        """
        try:
            account = Account.objects.get(email=email)
            if account.check_password(password):
                return account
        except Account.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            account = Account.objects.get(pk=user_id)
            if account.is_active:
                return account
            return None
        except Account.DoesNotExist:
            return None
