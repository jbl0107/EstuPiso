from rest_framework import serializers
from apis.models import *


class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = '__all__'
        

