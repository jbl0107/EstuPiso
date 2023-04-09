from rest_framework import serializers
from apis.models import *


class GroupReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupReservation
        fields = '__all__'
        extra_kwargs = {'student': {'write_only': True}}


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['student'] = instance.student.id
        return representation


    def validate_admin(self, value):

        if value:
            
            if value.isAdministrator == False:
                raise serializers.ValidationError('La solicitud debe ser gestionada por un administrador')

            return value
