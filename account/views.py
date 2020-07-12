from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from account.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    TODO: docs
    """

    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    filterset_fields = ["is_active", "is_superuser"]
    search_fields = ["^email"]
    ordering_fields = ["email", "is_active", "is_superuser", "date_joined"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.userid)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



class PasswordRecoverViewSet(viewsets.GenericViewSet):
    """
    """
    @action(
        methods=["post"],
        detail=False,
        url_path="forget-password",
        permission_classes=[permissions.AllowAny],
    )
    def forget_password(self, request):
        """
        Send an email with a link to resent password
        TODO: Implement serializer to validate email
        """
        User.objects.forget_password(request.data.get("email"))
        return Response({"sucess": True}, status=status.HTTP_200_OK)

    @action(
        methods=["post"],
        detail=False,
        url_path="reset-password",
        permission_classes=[permissions.AllowAny],
    )
    def reset_password(self, request):
        """
        Resets the forgotten password with user.password_reset_token
        TODO: Implement serializer to validate token and password
        """
        sucess = User.objects.reset_password(
            request.data.get("token"), request.data.get("password")
        )
        if sucess:
            return Response({"sucess": True}, status=status.HTTP_200_OK)
        return Response({"sucess": False}, status=status.HTTP_400_BAD_REQUEST)
