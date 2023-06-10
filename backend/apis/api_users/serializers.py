from rest_framework import serializers
from apis.models import User
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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
        
    def create(self, validate_data):
        user = User(**validate_data)
        user.set_password(validate_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user


