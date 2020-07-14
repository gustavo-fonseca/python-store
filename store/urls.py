from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

from account.urls import users_router
from client.urls import clients_router
from product.urls import products_router

# drf routes
router = routers.DefaultRouter(trailing_slash=False)
router.registry.extend(users_router.registry)
router.registry.extend(clients_router.registry)
router.registry.extend(products_router.registry)

# drf_yasg scheme view
schema_view = get_schema_view(
    openapi.Info(title="Python API Store", default_version="v0.1"),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    # api router urls
    path("", include(router.urls)),
    path("api-auth", include("rest_framework.urls")),
    # auth token urls
    path("login", obtain_jwt_token, name="login"),
    path("token-refresh", refresh_jwt_token, name="token-refresh"),
    path("token-verify", verify_jwt_token, name="token-verify"),
    path("docs", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
