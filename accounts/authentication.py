from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import Token

from django.contrib.auth.backends import ModelBackend


class EmailJwtAuthentication(JWTAuthentication):
    def get_user(self, validated_toke):
        User = get_user_model()
        user_id = validated_toke['user_id']
        return User.objects.get(pk = user_id)
    


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None