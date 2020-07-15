import uuid

from django.db import models


class Brand(models.Model):
    """
    Product's brand
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        "Name",
        max_length=240
    )
    is_active = models.BooleanField(
        "Is active",
        default=True
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Brand"
