from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='username', read_only=True)
    timestamp = serializers.DateTimeField(format="%b %d\' %y at %I:%M %p", read_only=True)
    class Meta:
        model = Message
        fields = ['sender', 'timestamp', 'text']