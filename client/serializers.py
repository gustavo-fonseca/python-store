from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core import validators
from client.models import ClientProfile

User = get_user_model()


class ClientProfileSerializer(serializers.ModelSerializer):
    """
    """

    email = serializers.ReadOnlyField(source="user.email")

    def validate_cellphone(self, value):
        """
        Checking if cellphone is in the right format
        """
        if not validators.cellphone_validate(value):
            raise serializers.ValidationError(
                "Cellphone has wrong format. Use this format instead: (00) 98888-7777"
            )
        return value

    class Meta:
        model = ClientProfile
        fields = [
            "id",
            "email",
            "name",
            "cpf",
            "gender",
            "date_birth",
            "date_joined",
            "cellphone",
        ]
        read_only_fields = ["id", "email", "cpf", "date_joined"]


class SignUpSerializer(serializers.ModelSerializer):
    """
    This serializer is used for clients to signup
    """

    email = serializers.EmailField(
        source="user.email",
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="This email address is already taken. please try another.",
            )
        ],
    )
    password = serializers.CharField(
        source="user.password",
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "password"},
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Repeat password"},
    )

    def validate_cellphone(self, value):
        """
        Checking if cellphone is in the right format
        """
        if not validators.cellphone_validate(value):
            raise serializers.ValidationError(
                "Cellphone has wrong format. Use this format instead: (00) 98888-7777"
            )
        return value

    def validate_cpf(self, value):
        """
        Checking if CPF is valid
        """
        if not validators.CPF_validate(value):
            raise serializers.ValidationError(
                "This CPF is not valid. Use this format: 000.000.000-00"
            )
        return value

    def validate_password(self, value):
        """
        Using native django password validation
        """
        password_validation.validate_password(value, self.instance)

        # Checking if passwords match
        if value != self.initial_data.get("password2"):
            raise serializers.ValidationError(
                "passwords did not match. Please try again."
            )
        return value

    def create(self, validate_data):
        """
        Removing password2 field to be able create the user
        """
        del validate_data["password2"]
        user_data = validate_data.pop("user")

        user = User.objects.create_user(**user_data)
        client = ClientProfile.objects.create(user=user, **validate_data)

        return client

    class Meta:
        model = ClientProfile
        fields = [
            "email",
            "password",
            "password2",
            "name",
            "cpf",
            "gender",
            "date_birth",
            "cellphone",
        ]
