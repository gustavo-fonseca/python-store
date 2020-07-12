from rest_framework import routers

from account.views import UserViewSet


users_router = routers.SimpleRouter(trailing_slash=False)
users_router.register(r'users', UserViewSet)
