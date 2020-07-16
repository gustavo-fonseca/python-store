from django.db import models


class OrderChoices(models.TextChoices):
    IN_PROGRESS = "IN_PROGRESS", "Shopping in progress"
    CONFIRMED = "CONFIRMED", "Confirmed"
    PAID = "PAID", "Paid"
