from rest_framework import routers

from client.views import SignUpViewSet, ClientProfileViewSer, ClientAddressViewSet


clients_router = routers.SimpleRouter(trailing_slash=False)
clients_router.register(r"signup", SignUpViewSet, basename="signup")
clients_router.register(r"client-profile", ClientProfileViewSer)
clients_router.register(r"client-address", ClientAddressViewSet)
