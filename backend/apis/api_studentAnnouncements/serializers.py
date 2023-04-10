from rest_framework import serializers
from apis.models import StudentAnnouncement


class StudentAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnnouncement
        fields = '__all__'
        extra_kwargs = {'student': {'write_only': True}}


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['student'] = instance.student.id
        return representation


