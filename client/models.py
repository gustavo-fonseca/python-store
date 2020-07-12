import uuid

from django.db import models
from django.contrib.auth import get_user_model

from core import constants

User = get_user_model()


class ClientProfile(models.Model):
    """
    TODO:
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.OneToOneField(
        User,
        verbose_name="User",
        related_name="clients_profile",
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



class ClientAddress(models.Model):
    """
    TODO:
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    clientprofile = models.ForeignKey(
        ClientProfile,
        related_name="address",
        on_delete=models.CASCADE
    )
    main = models.BooleanField(
        "Main address",
        default=True
    )
    name = models.CharField(
        "Name",
        max_length=150,
        help_text="Example: Grandma's House"
    )
    postal_code = models.CharField(
        "Postal Code",
        max_length=9,
    )
    address = models.CharField(
        "Address",
        max_length=250,
    )
    district = models.CharField(
        "District",
        max_length=250,
    )
    number = models.CharField(
        "Number",
        max_length=11,
        help_text="If not, type SN.",
    )
    city = models.CharField(
        "City",
        max_length=250,
    )
    state = models.CharField(
        "State",
        max_length=2,
        choices=constants.BRASIL_STATES_UF,
    )
    complement = models.CharField(
        "Complement",
        max_length=250,
        null=True,
        blank=True
    )
    landmark = models.CharField(
        "Landmark",
        max_length=250,
        null=True,
        blank=True
    )
