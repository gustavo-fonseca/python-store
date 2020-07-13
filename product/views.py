from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response

from core.permissions import IsAdminUserOrReadOnly
from product.models import Brand
from product.serializers import BrandSerializer

User = get_user_model()


class BrandViewSet(viewsets.ModelViewSet):
    """
    TODO: docs
    """

    queryset = Brand.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = BrandSerializer
    filterset_fields = ["name", "is_active"]
    search_fields = ["^name"]
    ordering_fields = ["name", "is_active"]

    def get_queryset(self):
        return Brand.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
