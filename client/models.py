import uuid

from django.db import models
from django.contrib.auth import get_user_model

from core import constants

User = get_user_model()


class ClientProfile(models.Model):
    """
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        User,
        verbose_name="User",
        related_name="client_profile",
        on_delete=models.CASCADE
    )
    name = models.CharField(
        "Name",
        max_length=150
    )
    cpf = models.CharField(
        "CPF",
        max_length=14
    )
    gender = models.CharField(
        "Gender",
        max_length=1,
        choices=constants.GENDER
    )
    cellphone = models.CharField(
        "Cellphone",
        max_length=16
    )
    date_birth = models.DateField(
        "Birthday"
    )
    date_joined = models.DateTimeField(
        "Date joined",
        auto_now_add=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Client's Profile"
