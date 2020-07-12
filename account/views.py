from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from account.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    TODO: docs
    """

    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
