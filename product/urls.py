from rest_framework import routers

from product.views import BrandViewSet


products_router = routers.SimpleRouter(trailing_slash=False)
products_router.register(r"product-brands", BrandViewSet)
