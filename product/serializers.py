from django.contrib.auth import get_user_model
from rest_framework import serializers

from product.models import Brand

User = get_user_model()


class BrandSerializer(serializers.ModelSerializer):
    """
    TODO:
    """

    class Meta:
        model = Brand
        fields = ["id", "name", "is_active"]
        read_only_fields = ["id"]
