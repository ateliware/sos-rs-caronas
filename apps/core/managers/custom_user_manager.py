from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, cpf, password=None):
        """
        Creates and saves a User with the given cpf and password.
        """
        if not cpf:
            raise ValueError("Users must have an cpf number")

        if not password:
            raise ValueError("Users must have a password")

        user = self.model(cpf=cpf)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, password=None):
        """
        Creates and saves a superuser with the given cpf and password.
        """
        user = self.create_user(
            cpf=cpf,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
