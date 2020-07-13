from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, mixins, status
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


class ClientProfileViewSer(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin, viewsets.GenericViewSet):
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


class ClientAddressViewSet(viewsets.ModelViewSet):
    """
    TODO:
    """

    queryset = ClientAddress.objects.all()
    permission_classes = [IsClientProfileOwner]
    serializer_class = ClientAddressSerializer
    filterset_fields = ["name", "postal_code", "district", "city", "state", "main"]
    search_fields = ["^name", "^postal_code", "^district", "^city", "state"]
    ordering_fields = ["district", "city", "state", "main"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ClientAddress.objects.filter(is_deleted=False)
        return ClientAddress.objects.filter(
            is_deleted=False,
            client_profile=self.request.user.client_profile
        )

    def perform_create(self, serializer):
        serializer.save(client_profile=self.request.user.client_profile)
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
