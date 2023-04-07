from .models import Student, Owner
from rest_framework.permissions import BasePermission



class IsStudentOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and Student.objects.filter(id=request.user.id).exists()) or (request.user.isAdministrator and request.user.is_authenticated) 
    


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and Owner.objects.filter(id=request.user.id).exists()) or (request.user.isAdministrator and request.user.is_authenticated) 
    

