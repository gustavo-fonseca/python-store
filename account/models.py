import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from account.managers import CustomUserManager


class User(AbstractUser):
    """
    This model will be used for both admin and client users
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(
        "Email",
        unique=True
    )
    password_reset_token = models.UUIDField(
        "Password's reset token",
        null=True,
        blank=True,
        unique=True,
        help_text="This token will be send to email for reseting password"
    )
    password_reset_token_expiration_datetime = models.DateTimeField(
        "Password's reset token expiration datetime delta",
        null=True,
        blank=True,
        help_text="Used to expire password's reset token"
    )

    # Removing unnecessary AbstractUser`s fields
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


