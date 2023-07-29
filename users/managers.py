from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, identifier, password, **extra_fields):
        if not identifier or len(identifier) <= 0:
            raise ValueError("Identifier field is required!")
        if not password:
            raise ValueError("Password field is required!")

        user = self.model(identifier=identifier, **extra_fields)
        user.password = make_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, identifier, password, **extra_fields):
        user = self.create_user(identifier=identifier, password=password, **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user

