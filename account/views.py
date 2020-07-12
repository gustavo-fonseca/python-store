from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from account.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    TODO: docs
    """

    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
       instance.is_active = False
       instance.save()
       return Response(status=status.HTTP_204_NO_CONTENT)
