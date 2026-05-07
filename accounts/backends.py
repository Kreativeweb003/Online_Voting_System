from .models import User
from django.contrib.auth.hashers import check_password


class CustomAuthBackend:
    def authenticate(self, request, username=None, password=None):

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(voter_id=username)
            except User.DoesNotExist:
                return None

        if user and check_password(password, user.password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
            
            
            







