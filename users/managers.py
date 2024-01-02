from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, identifier, password, last_name, first_name, middle_name, **extra_fields):
        if not identifier or len(identifier) <= 0:
            raise ValueError("Identifier field is required!")
        if not password:
            raise ValueError("Password field is required!")

        user = self.model(identifier=identifier, **extra_fields)
        user.password = make_password(password)
        user.last_name = last_name
        user.first_name = first_name
        user.middle_name = middle_name
        user.save(using=self.db)
        return user

    def create_superuser(self, identifier, password, last_name, first_name, middle_name, **extra_fields):
        user = self.create_user(identifier=identifier, password=password, last_name=last_name,
                                first_name=first_name, middle_name=middle_name, **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.type = "Администратор"
        user.save(using=self.db)
        return user

