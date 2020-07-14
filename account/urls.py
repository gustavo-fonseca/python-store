from rest_framework import routers

from account.views import UserViewSet, ForgetPasswordViewSet, \
    ResetPasswordViewSet


users_router = routers.SimpleRouter(trailing_slash=False)
users_router.register(r'users', UserViewSet)
users_router.register(r'auth', ForgetPasswordViewSet)
users_router.register(r'auth', ResetPasswordViewSet)
