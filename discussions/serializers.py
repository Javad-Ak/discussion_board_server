from rest_framework import serializers

from discussions.models import Topic, Comment


class TopicSerializer(serializers.ModelSerializer):
    """Serializer for the Topic model"""
    user = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Topic
        exclude = ['owner']
        extra_kwargs = {'pk': {'read_only': True}, 'owner': {'read_only': True}}


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model"""
    user = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        exclude = ['owner']
        extra_kwargs = {'pk': {'read_only': True}, 'topic': {'read_only': True}}
