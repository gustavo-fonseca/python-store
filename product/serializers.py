from django.contrib.auth import get_user_model
from rest_framework import serializers

from product.models import Brand, Category

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
