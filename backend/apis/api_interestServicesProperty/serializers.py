from rest_framework import serializers
from apis.models import *


class InterestServicePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestServiceProperty
        fields = '__all__'


