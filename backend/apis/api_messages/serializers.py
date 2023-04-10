from rest_framework import serializers
from apis.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        extra_kwargs = {'userSender': {'write_only': True}}


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['userSender'] = instance.userSender.id
        return representation

