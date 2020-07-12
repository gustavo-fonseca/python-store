from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from account.urls import users_router
from client.urls import clients_router

router = routers.DefaultRouter(trailing_slash=False)
router.registry.extend(users_router.registry)
router.registry.extend(clients_router.registry)

urlpatterns = [
    # api router urls
    path("", include(router.urls)),
    # django admin urls
    path("admin/", admin.site.urls),
    # DRF browseble api login urls
    path("api-auth", include("rest_framework.urls")),
    # auth token urls
    path("login", obtain_jwt_token),
    path("token-refresh", refresh_jwt_token),
    path("token-verify", verify_jwt_token),
]
