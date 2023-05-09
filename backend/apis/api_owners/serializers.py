from rest_framework import serializers
from apis.models import Owner
import re


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'



    def validate_dni(self, value):
        nif_regex = re.compile(r'^[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKE]$', re.IGNORECASE)
        nie_regex = re.compile(r'^[XYZ][0-9]{7}[TRWAGMYFPDXBNJZSQVHLCKE]$', re.IGNORECASE)
        if not nif_regex.match(value) and not nie_regex.match(value):
            raise serializers.ValidationError('El formato del DNI no es válido')
        return value
    

    def validate_password(self, value):

        if value:
            if len(value) < 8:
                raise serializers.ValidationError('La contraseña debe tener al menos 8 caracteres')
            
            return value
        

    def validate_isAdministrator(self, value):
        if value:
            raise serializers.ValidationError('Un propietario no puede ser administrador')
            
        return value


    def create(self, validate_data):
        owner = Owner(**validate_data)
        owner.set_password(validate_data['password'])
        owner.save()
        return owner
    
    def update(self, instance, validated_data):
        updated_owner = super().update(instance, validated_data)
        updated_owner.set_password(validated_data['password'])
        updated_owner.save()
        return updated_owner




class OwnerPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['username', 'photo', 'name']
