from django.db import models

from product.models.category import Category
from product.models.brand import Brand
from product.models.image import Image


class Product(models.Model):
    """
    The product to sale
    """
    brand = models.ForeignKey(
        Brand,
        verbose_name="Brand",
        related_name="products",
        on_delete=models.SET_NULL,
        null=True
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name="Categories",
        related_name="products"
    )
    images = models.ManyToManyField(
        Image,
        verbose_name="Images",
        related_name="images"
    )
    slug = models.SlugField(
        "URL slug",
        max_length=250,
        unique=True,
        null=True,
        blank=True
    )
    name = models.CharField(
        "Name",
        max_length=240
    )
    is_active = models.BooleanField(
        "Is active",
        default=True
    )

    # technical features
    short_description = models.TextField(
        "Short description",
        null=True,
        blank=True
    )
    full_description = models.TextField(
        "Full description",
        null=True,
        blank=True
    )
    color_hex = models.CharField(
        "Color",
        max_length=7,
        null=True,
        blank=True
    )

    # prices
    price = models.DecimalField(
        "Price",
        max_digits=10,
        decimal_places=2
    )
    old_price = models.DecimalField(
        "Old price",
        max_digits=10,
        decimal_places=2
    )
    cost_price = models.DecimalField(
        "cost price",
        max_digits=10,
        decimal_places=2
    )

    # quantity of a product that is available for sale
    inventory = models.IntegerField(
        "Inventory",
        default=0
    )

    # Delivery info
    weight_grams = models.IntegerField(
        "Weight in grams",
    )
    length_mm = models.IntegerField(
        "Length in millimeters",
    )
    width_mm = models.IntegerField(
        "Width in millimeters",
    )
    thickness_mm = models.IntegerField(
        "Thickness/Depth in millimeters",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Product"
    