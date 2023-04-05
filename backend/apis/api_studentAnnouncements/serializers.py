from rest_framework import serializers
from apis.models import *


class StudentAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnnouncement
        fields = '__all__'


