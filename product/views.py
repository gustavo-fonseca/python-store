from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response

from core.permissions import IsAdminUserOrReadOnly
from product.models import Brand, Category, Image
from product.serializers import BrandSerializer, CategorySerializer, ImageSerializer

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


class CategoryViewSet(viewsets.ModelViewSet):
    """
    TODO: docs
    """

    queryset = Category.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = CategorySerializer
    filterset_fields = ["name", "parent", "is_active"]
    search_fields = ["^name"]
    ordering_fields = ["name", "is_active"]

    def get_queryset(self):
        return Category.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageViewSet(viewsets.ModelViewSet):
    """
    TODO: docs
    """

    queryset = Image.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = ImageSerializer

    def get_queryset(self):
        return Image.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
