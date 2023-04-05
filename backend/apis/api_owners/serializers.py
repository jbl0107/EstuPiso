from rest_framework import serializers
from apis.models import *


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


    def validate_password(self, value):

        if value:
            if len(value) < 8:
                raise serializers.ValidationError('Password must be at least 8 characters')
            
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

