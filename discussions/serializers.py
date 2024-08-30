from rest_framework import serializers

from discussions.models import Topic, Comment


class TopicSerializer(serializers.ModelSerializer):
    """Serializer for the Topic model"""
    username = serializers.ReadOnlyField(source='owner.username')
    avatar = serializers.ImageField(source='owner.avatar', read_only=True)

    class Meta:
        model = Topic
        exclude = ['owner']
        extra_kwargs = {'pk': {'read_only': True},}


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model"""
    username = serializers.ReadOnlyField(source='owner.username')
    avatar = serializers.ImageField(source='owner.avatar', read_only=True)

    class Meta:
        model = Comment
        exclude = ['owner', 'topic']
        extra_kwargs = {'pk': {'read_only': True},}
