from rest_framework import serializers
from apis.models import *


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


    def validate_password(self, value):

        if value:
            if len(value) < 8:
                raise serializers.ValidationError('Password must be at least 8 characters')
            
            return value
        
    def create(self, validate_data):
        student = Student(**validate_data)
        student.set_password(validate_data['password'])
        student.save()
        return student
    
    def update(self, instance, validated_data):
        updated_student = super().update(instance, validated_data)
        updated_student.set_password(validated_data['password'])
        updated_student.save()
        return updated_student

