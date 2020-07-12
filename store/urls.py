from django.contrib import admin
from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    # api router urls
    path("", include(router.urls)),
    # django admin urls
    path("admin/", admin.site.urls),
    # DRF browseble api login urls
    path("api-auth/", include("rest_framework.urls")),
]
