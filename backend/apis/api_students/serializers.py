from rest_framework import serializers
from apis.models import Student
import re


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
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
            raise serializers.ValidationError('Un estudiante no puede ser administrador')
            
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

