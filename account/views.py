# from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model, password_validation
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from account.serializers import UserSerializer, ForgetPasswordSerializer, \
    ResetPasswordSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    Full rest api actions for user
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


class ForgetPasswordViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ForgetPasswordSerializer

    @action(
        methods=["post"],
        detail=False,
        url_path="forget-password",
        url_name="forget-password",
        permission_classes=[permissions.AllowAny],
    )
    def forget_password(self, request):
        """
        Send an email with a token to reset password in /auth/reset-password action
        """
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer

    @action(
        methods=["post"],
        detail=False,
        url_path="reset-password",
        url_name="reset-password",
        permission_classes=[permissions.AllowAny],
    )
    def reset_password(self, request):
        """
        Reset the password for a user who match the given token
        """
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

