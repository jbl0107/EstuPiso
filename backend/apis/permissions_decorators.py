from .models import Student, Owner
from rest_framework.permissions import BasePermission



class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and Student.objects.filter(id=request.user.id).exists()
    


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and Owner.objects.filter(id=request.user.id).exists()
     