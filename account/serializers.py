from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
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
        fields = ["id", "email", "password", "is_superuser", "is_active", "date_joined"]
        read_only_fields = ["id", "date_joined"]
        extra_kwargs = {"password": {"write_only": True, "required": True}}

