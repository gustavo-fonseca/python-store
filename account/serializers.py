from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    TODO: docs
    """

    class Meta:
        model = User
        fields = ["id", "email", "password", "is_superuser", "is_active"]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}

