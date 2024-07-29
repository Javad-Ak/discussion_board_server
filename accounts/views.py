from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated

from . import serializers
from .models import User


class HasSamePK(BasePermission):
    message = 'You are not the owner of this account.'

    def has_object_permission(self, request, view, obj):
        try:
            return request.user is not None and request.user.pk == obj.pk
        except AttributeError:
            return False


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """User and profile management"""
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            serializer_class = serializers.UserRegistrationSerializer
        else:
            serializer_class = serializers.UserSerializer
        return serializer_class

    def get_permissions(self):
        if self.action in ('create', 'retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
