from rest_framework import serializers
from messages.models import Message


class MessageShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id'
                  , 'timestamp'
                  , 'level'
                  , 'source'
                  , 'message'
        )


class MessageFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id'
                  , 'timestamp'
                  , 'level'
                  , 'source'
                  , 'message'
                  , 'filename'
                  , 'line_number'
                  , 'session'
                  , 'payload'
        )