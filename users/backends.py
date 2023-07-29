from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from users.models import BaseUser


class IdentifierBackend(BaseBackend):
    def authenticate(self, request, identifier=None, password=None, **kwargs):
        UserModel = get_user_model()
        if identifier is None:
            identifier = kwargs.get(UserModel.USERNAME_FIELD)
        if identifier is None or password is None:
            return
        try:
            user = UserModel.objects.get(identifier=identifier)
        except UserModel.DoesNotExist:
            return "Пользователь не существует"
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        return BaseUser.objects.get(identifier=user_id)