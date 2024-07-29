from rest_framework import viewsets, mixins, status, views
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers
from .models import User


class HasSamePK(BasePermission):
    message = 'You are not the owner of this account.'

    def has_object_permission(self, request, view, obj):
        try:
            return request.user is not None and request.user.pk == obj.pk
        except AttributeError:
            return False


class LogoutView(views.APIView):
    """
    logs out the user from all systems.
    Run 'python manage.py flushexpiredtokens' on a daily basis.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response("Successful Logout", status=status.HTTP_200_OK)


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """User and profile management"""
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.UserRegistrationSerializer
        else:
            return serializers.UserSerializer

    def get_permissions(self):
        if self.action in ('create', 'retrieve'):
            return [AllowAny]
        else:
            return [HasSamePK]
