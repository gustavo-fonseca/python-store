import uuid

from django.db import models


class Image(models.Model):
    """
    Product's image
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    file = models.FileField(
        "Image file",
        upload_to="products-images/"
    )
    is_active = models.BooleanField(
        "Is active",
        default=True
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Image"
