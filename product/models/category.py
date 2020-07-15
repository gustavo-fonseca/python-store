import uuid

from django.db import models


class Category(models.Model):
    """
    Product's category
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
    parent = models.ForeignKey(
        "self",
        verbose_name="Parent",
        related_name="children",
        on_delete=models.SET_NULL,
        null=True
    )
    is_active = models.BooleanField(
        "Is active",
        default=True
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
