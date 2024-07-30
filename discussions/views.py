from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import BasePermission

from discussions.models import Topic, Comment
from discussions.serializers import TopicSerializer, CommentSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class IsOwner(BasePermission):
    message = 'You are not the owner of this object.'

    def has_object_permission(self, request, view, obj):
        try:
            return request.user and not isinstance(request.user, AnonymousUser) and obj.owner == request.user
        except AttributeError:
            return False


class TopicViewSet(viewsets.ModelViewSet):
    """topic view set: list, create, update, partial_update, destroy, retrieve"""
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny]
        elif self.action == 'create':
            return [IsAuthenticated]
        else:
            return [IsOwner]


class CommentListCreateView(viewsets.ModelViewSet):
    """comment view set: list, create, update, partial_update, destroy, retrieve"""
    serializer_class = CommentSerializer

    def get_queryset(self):
        self.queryset = Comment.objects.all().filter(topic_id=self.kwargs.get('topic_id'))
        return self.queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny]
        elif self.action == 'create':
            return [IsAuthenticated]
        else:
            return [IsOwner]
