from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response

from account.permissions import IsUserOwnerAdmin
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
    Create a client's profile and it's user
    """

    queryset = ClientProfile.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SignUpSerializer


class ClientProfileViewSer(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Client's profile viewser that implements list, retrieve and update actions 
    """

    queryset = ClientProfile.objects.all()
    permission_classes = [IsUserOwnerAdmin]
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
    Client's address viewset that implements full model viewset actions
    """

    queryset = ClientAddress.objects.all()
    permission_classes = [IsClientProfileOwner]
    serializer_class = ClientAddressSerializer
    filterset_fields = ["name", "postal_code", "district", "city", "state", "main"]
    search_fields = ["^name", "^postal_code", "^district", "^city", "state"]
    ordering_fields = ["district", "city", "state", "main"]

    def get_queryset(self):
        queryset = ClientAddress.objects.filter(is_deleted=False)
        if not self.request.user.is_superuser:
            return queryset.filter(client_profile=self.request.user.client_profile)
        return queryset

    def perform_create(self, serializer):
        serializer.save(client_profile=self.request.user.client_profile)
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.date_deleted = timezone.now()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
