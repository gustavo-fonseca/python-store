from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer for full CRUD actions
    """

    def get_fields(self, *args, **kwargs):
        """
        Make password field required only for PUT and PATCH http methods
        """
        fields = super(UserSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get("request", None)
        if request and request.method in ["PUT", "PATCH"]:
            fields["password"].required = False
        return fields

    class Meta:
        model = User
        fields = ["id", "email", "password", "is_superuser", "is_active",
                  "date_joined"]
        read_only_fields = ["id", "date_joined"]
        extra_kwargs = {"password": {"write_only": True, "required": True}}


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def save(self):
        email = self.validated_data['email']
        User.objects.forget_password(email)

    class Meta:
        fields = ["email"]


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.UUIDField(required=True)
    password = serializers.CharField(required=True)

    def validate_token(self, value):
        """
        Ensure the given token is valid
        """
        if not User.objects.is_reset_password_token_valid(value):
            raise serializers.ValidationError(
                "The given token is not valid or outdated. "
                "Please request a new token."
            )
        return value

    def validate_password(self, value):
        """
        Using native django password validation
        """
        password_validation.validate_password(value)
        return value

    def save(self):
        """
        Override serializer save method to reset user password
        Return True if success
        """
        token = self.validated_data['token']
        password = self.validated_data['password']
        return User.objects.reset_password(token, password)

    class Meta:
        fields = ["token", "password"]
