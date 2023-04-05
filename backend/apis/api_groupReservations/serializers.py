from rest_framework import serializers
from apis.models import *


class GroupReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupReservation
        fields = '__all__'


    def validate_admin(self, value):

        if value:
            
            if value.isAdministrator == False:
                raise serializers.ValidationError('La solicitud debe ser gestionada por un administrador')

            return value
