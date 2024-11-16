# autenticacion/backends.py
from django.contrib.auth.backends import BaseBackend
from .models import User

class NameDniBackend(BaseBackend):
    def authenticate(self, request, name=None, 
                     surname=None ,  dni=None,  **kwargs):
        try:
            user = User.objects.get(name=name, dni=dni, surname=surname)
            if user.check_password(dni):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id )
        except User.DoesNotExist:
            return None