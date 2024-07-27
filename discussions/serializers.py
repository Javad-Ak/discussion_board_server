from rest_framework import serializers

from discussions.models import Topic, Comment


class TopicSerializer(serializers.ModelSerializer):
    """Serializer for the Topic model"""

    class Meta:
        model = Topic
        fields = '__all__'
        extra_kwargs = {'pk': {'read_only': True}}


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model"""

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'pk': {'read_only': True}}
