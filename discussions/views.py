from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, generics
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
    queryset = Topic.objects.all().order_by('date_added').reverse()
    serializer_class = TopicSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        return serializer.save(owner_id=self.request.user.pk)


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        self.queryset = (Comment.objects.all()
                         .filter(topic_id=self.kwargs.get('topic_id'))
                         .order_by('date_added').reverse())
        return self.queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        return serializer.save(owner_id=self.request.user.pk, topic_id=self.kwargs.get('topic_id'))


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        self.queryset = (Comment.objects.all()
                         .filter(topic_id=self.kwargs.get('topic_id'))
                         .order_by('date_added').reverse())
        return self.queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsOwner]
        return [permission() for permission in self.permission_classes]


class SearchView(generics.ListAPIView):
    serializer_class = TopicSerializer

    def get_queryset(self):
        self.queryset = Topic.objects.filter(title__contains=self.kwargs.get('query')).order_by('date_added').reverse()
        return self.queryset
