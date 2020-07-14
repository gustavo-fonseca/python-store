from rest_framework import routers

from account.views import UserViewSet, PasswordRecoverViewSet


users_router = routers.SimpleRouter(trailing_slash=False)
users_router.register(r'users', UserViewSet)
users_router.register(r'auth', PasswordRecoverViewSet, basename="user")
