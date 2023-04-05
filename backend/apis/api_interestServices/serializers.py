from rest_framework import serializers
from apis.models import *


class InterestServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestService
        fields = '__all__'


