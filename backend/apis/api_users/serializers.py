from rest_framework import serializers
from apis.models import *

####### Users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


    def validate_password(self, value):

        if value:
            if len(value) < 8:
                raise serializers.ValidationError('Password must be at least 8 characters')
            
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
#######

