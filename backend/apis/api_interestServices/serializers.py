from rest_framework import serializers
from apis.models import InterestService


class InterestServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestService
        fields = '__all__'


