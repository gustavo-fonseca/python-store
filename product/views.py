from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response

from account.permissions import IsAdminUserOrReadOnly
from product.models import Brand, Category, Image, Product
from product.serializers import BrandSerializer, CategorySerializer, \
     ImageSerializer, ProductSerializer

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
        # queryset just for schema generation metadata
        if getattr(self, 'swagger_fake_view', False):
            return Brand.objects.none()
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
        # queryset just for schema generation metadata
        if getattr(self, 'swagger_fake_view', False):
            return Category.objects.none()
        
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
        # queryset just for schema generation metadata
        if getattr(self, 'swagger_fake_view', False):
            return Image.objects.none()
        
        return Image.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ModelViewSet):
    """
    TODO: docs
    """

    queryset = Product.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = ProductSerializer

    def get_queryset(self):
        # queryset just for schema generation metadata
        if getattr(self, 'swagger_fake_view', False):
            return Product.objects.none()
        
        return Product.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

