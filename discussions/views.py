from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import BasePermission

from discussions.models import Topic, Comment
from discussions.serializers import TopicSerializer, CommentSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class IsOwner(BasePermission):
    message = 'You are not the owner of this object.'

    def has_object_permission(self, request, view, obj):
        try:
            return request.user is not None and obj.owner == request.user
        except AttributeError:
            return False


class TopicViewSet(viewsets.ModelViewSet):
    """topic view set: list, create, update, partial_update, destroy, retrieve"""
    model = Topic
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny]
        elif self.action == 'create':
            return [IsAuthenticated]
        else:
            return [IsOwner]


class CommentListCreateView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all().filter(topic_id=self.kwargs.get('topic_pk'))
        return queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny]
        elif self.request.method == 'POST':
            return [IsAuthenticated]


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny]
        elif:
            return [IsOwner]
