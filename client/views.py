from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from account.permissions import IsUserOwner
from client.permissions import IsClientProfileOwner
from client.serializers import (
    SignUpSerializer,
    ClientProfileSerializer,
    ClientAddressSerializer,
)
from client.models import ClientProfile, ClientAddress

User = get_user_model()


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    TODO: docs
    """

    queryset = ClientProfile.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SignUpSerializer


class ClientProfileViewSer(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    TODO: docs
    """

    queryset = ClientProfile.objects.all()
    permission_classes = [IsUserOwner]
    serializer_class = ClientProfileSerializer
    filterset_fields = [
        "name",
        "cpf",
        "gender",
        "date_birth",
        "cellphone",
        "date_joined",
    ]
    search_fields = ["^name", "^cpf"]
    ordering_fields = ["name", "gender", "date_birth", "date_joined"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ClientProfile.objects.all()
        return ClientProfile.objects.filter(user=self.request.user)

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


class ClientAddressViewSet(viewsets.ModelViewSet):
    """
    TODO:
    """

    queryset = ClientAddress.objects.all()
    permission_classes = [IsClientProfileOwner]
    serializer_class = ClientAddressSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ClientAddress.objects.all()
        return ClientAddress.objects.filter(
            clientprofile=self.request.user.clients_profile.first()
        )

# TRABALHANDO NO ADDRESS E USER - TESTAR NO POSTMAN