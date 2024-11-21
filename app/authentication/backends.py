from django.contrib.auth.backends import BaseBackend
from .models import User, encrypt_cbc, key
import logging
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
class AuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            encrypted_username = encrypt_cbc(username, key)
            user = User.objects.get(dni=encrypted_username)
            logger.error(f"User: {user.name}, {user.password}")
            logger.error(f"Password: {user.check_password(password)}")
            if user.check_password(password):
                logger.error(f"Authentication success for dni: {username}")
                return user
        except User.DoesNotExist:
            return None
    
    def authenticate(self, request, dni=None, **kwargs):
        try:
            user = User.objects.get(dni=dni)
            if user.check_password(dni):
                return user
        except User.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
