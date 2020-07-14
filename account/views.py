# from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model, password_validation
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from account.serializers import UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    Implements the full CRUD for user model
    """

    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    filterset_fields = ["is_active", "is_superuser"]
    search_fields = ["^email"]
    ordering_fields = ["email", "is_active", "is_superuser", "date_joined"]

    def get_queryset(self):
        # queryset just for schema generation metadata
        if getattr(self, 'swagger_fake_view', False):
            return User.objects.none()

        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordRecoverViewSet(viewsets.GenericViewSet):
    """
    Implements forget password actions
    """

    def get_serializer_class(self):
        # queryset just for schema generation metadata
        if getattr(self, 'swagger_fake_view', False):
            return UserSerializer
    
    @action(
        methods=["post"],
        detail=False,
        url_path="forget-password",
        url_name="forget-password",
        permission_classes=[permissions.AllowAny],
    )
    def forget_password(self, request):
        """
        Send an email with a link to resent password
        """
        User.objects.forget_password(request.data.get("email"))
        return Response({"success": True}, status=status.HTTP_200_OK)

    @action(
        methods=["post"],
        detail=False,
        url_path="reset-password",
        url_name="reset-password",
        permission_classes=[permissions.AllowAny],
    )
    def reset_password(self, request):
        """
        Resets the forgotten password with user.password_reset_token
        """
        try:
            password_validation.validate_password(request.data.get("password"))
        except Exception as e:
            return Response({"password": e}, status=status.HTTP_400_BAD_REQUEST)

        reset_success = User.objects.reset_password(
            request.data.get("token"), request.data.get("password")
        )
        if reset_success:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
