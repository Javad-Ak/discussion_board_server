from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, mixins, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response

from . import serializers
from .models import User


class IsSamePerson(BasePermission):
    message = 'You are not the owner of this account.'

    def has_object_permission(self, request, view, obj):
        try:
            return request.user and not isinstance(request.user, AnonymousUser) and request.user.pk == obj.pk
        except AttributeError:
            return False


class UserViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """User management view"""
    queryset = User.objects.all()
    serializer_class = serializers.UserPublicSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsSamePerson]
        return [permission() for permission in self.permission_classes]

    @action(methods=['POST'], detail=False, permission_classes=[IsSamePerson])
    def password(self, request):
        user = request.user
        self.check_object_permissions(request, user)

        serializer = serializers.ChangePasswordSerializer(data=request.data)

        if serializer.is_valid() and user:
            old_password = serializer.data.get("old_password")
            if not user.check_password(old_password):
                return Response({"message": "Old password is wrong"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request):
        # TODO: email recovery
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountRecoveryView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request):
        # TODO: email recovery
        pass
