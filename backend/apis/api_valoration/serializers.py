from rest_framework import serializers
from apis.models import *


class UserValorationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserValoration
        fields = '__all__'
        extra_kwargs = {'valuer': {'write_only': True}}


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['valuer'] = instance.valuer.id
        return representation


    def validate_valuer(self, value):
        if value:
            if value.isAdministrator:
                raise serializers.ValidationError('Un administrador no puede realizar valoraciones')
            
            return value
        
    def validate_valued(self, value):
        if value:
            if value.isAdministrator:
                raise serializers.ValidationError('Un administrador no puede recibir valoraciones')
            
            return value
        

class PropertyValorationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyValoration
        fields = '__all__'
        extra_kwargs = {'valuer': {'write_only': True}}


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['valuer'] = instance.valuer.id
        return representation


    def validate_valuer(self, value):
        if value:
            if value.isAdministrator:
                raise serializers.ValidationError('Un administrador no puede realizar valoraciones')
            
            return value