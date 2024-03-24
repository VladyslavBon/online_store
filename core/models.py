from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(
        self, email, first_name, last_name, phone_number, password, **extra_fields
    ):
        if not email:
            raise ValueError("The Email field must be set")
        if not first_name:
            raise ValueError("The First Name field must be set")
        if not last_name:
            raise ValueError("The Last Name field must be set")
        if not phone_number:
            raise ValueError("The Phone Number field must be set")
        if not password:
            raise ValueError("The Password field must be set")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, last_name, phone_number, password, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email, first_name, last_name, phone_number, password, **extra_fields
        )


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    phone_number = models.CharField(
        unique=True, max_length=20, validators=[RegexValidator]
    )
    image = models.ImageField(upload_to="images/", blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    def __str__(self):
        return self.email
