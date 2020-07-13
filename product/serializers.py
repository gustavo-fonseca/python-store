from django.contrib.auth import get_user_model
from rest_framework import serializers

from product.models import Brand, Category, Image, Product

User = get_user_model()


class BrandSerializer(serializers.ModelSerializer):
    """
    TODO:
    """

    class Meta:
        model = Brand
        fields = ["id", "name", "is_active"]
        read_only_fields = ["id"]


class CategorySerializer(serializers.ModelSerializer):
    """
    TODO:
    """

    class Meta:
        model = Category
        fields = ["id", "name", "parent", "is_active"]
        read_only_fields = ["id"]


class ImageSerializer(serializers.ModelSerializer):
    """
    TODO:
    """

    class Meta:
        model = Image
        fields = ["id", "file", "is_active"]
        read_only_fields = ["id"]


class ProductSerializer(serializers.ModelSerializer):
    """
    TODO:
    """

    class Meta:
        model = Product
        fields = [
            "id",
            "brand",
            "categories",
            "slug",
            "name",
            "is_active",
            "short_description",
            "full_description",
            "color_hex",
            "price",
            "old_price",
            "cost_price",
            "inventory",
            "weight_grams",
            "length_mm",
            "width_mm",
            "thickness_mm",
        ]
        read_only_fields = ["id", "slug"]
