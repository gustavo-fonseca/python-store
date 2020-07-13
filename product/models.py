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
        return self.name
    
    class Meta:
        verbose_name = "Brand"


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
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


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
        return str(self.id)

    class Meta:
        verbose_name = "Image"


class Product(models.Model):
    """
    The product to sale
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
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
    slug = models.SlugField(
        "URL slug",
        max_length=250,
        unique=True
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
        return self.name
    
    class Meta:
        verbose_name = "Product"
    
