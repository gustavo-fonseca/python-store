from rest_framework import routers

from product.views import (BrandViewSet, CategoryViewSet, ImageViewSet,
                           ProductViewSet)


products_router = routers.SimpleRouter(trailing_slash=False)
products_router.register(r"products", ProductViewSet)
products_router.register(r"product-brands", BrandViewSet)
products_router.register(r"product-categories", CategoryViewSet)
products_router.register(r"product-images", ImageViewSet)
