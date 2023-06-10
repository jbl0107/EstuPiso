from .models import Student, Owner
from rest_framework.permissions import BasePermission



class IsStudentOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and Student.objects.filter(id=request.user.id).exists()) or (request.user.isAdministrator and request.user.is_authenticated) 
    


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and Owner.objects.filter(id=request.user.id).exists()) or (request.user.isAdministrator and request.user.is_authenticated) 
    

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and Owner.objects.filter(id=request.user.id).exists()
    


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and Student.objects.filter(id=request.user.id).exists()


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.isAdministrator and request.user.is_authenticated
    
