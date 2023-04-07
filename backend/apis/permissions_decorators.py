from rest_framework import permissions
from .models import Student, Owner

def is_student(user):
    return user.is_authenticated and user.is_instance_of(Student)

def is_owner(user):
    return user.is_authenticated and user.is_instance_of(Owner)

class AccesoEstudiante(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_student(request.user)

class AccesoPropietario(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_owner(request.user)
