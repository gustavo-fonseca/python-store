import uuid

from django.db import models
from django.contrib.auth import get_user_model

from client.models.client import ClientProfile
from core import constants

User = get_user_model()


class ClientAddress(models.Model):
    """
    Client's address model
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    client_profile = models.ForeignKey(
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
        max_length=150,
    )
    number = models.CharField(
        "Number",
        max_length=8,
        help_text="If not, type SN.",
    )
    city = models.CharField(
        "City",
        max_length=100,
    )
    state = models.CharField(
        "State",
        max_length=2,
        choices=constants.BRASIL_STATES_UF,
    )
    complement = models.CharField(
        "Complement",
        max_length=100,
        null=True,
        blank=True
    )
    landmark = models.CharField(
        "Landmark",
        max_length=100,
        null=True,
        blank=True
    )
    date_created = models.DateTimeField(
        "Date created",
        auto_now_add=True,
    )
    date_updated = models.DateTimeField(
        "Date updated",
        auto_now=True
    )
    is_deleted = models.BooleanField(
        "Deleted",
        default=False
    )
    date_deleted = models.DateTimeField(
        "Date deleted",
        null=True
    )

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        """
        Compute the main address
        """
        main_address = ClientAddress.objects.filter(
            main=True,
            client_profile=self.client_profile
        )
        # make sure that just one address will be main
        if self.main:
            main_address.update(main=False)

        # If there isn't a main address force the current\
        # created/updated to be the main
        if not main_address.count():
            self.main = True
        super(ClientAddress, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Client's Address"
        verbose_name_plural = "Client's Address"
