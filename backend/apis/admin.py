from django.contrib import admin
from .models import *

class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'type', 'size', 'price']
    list_filter = ['type', 'owner']

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'surname', 'email', 'telephone']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'surname', 'email', 'telephone']

class OwnerAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'surname', 'email', 'telephone']


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['owner', 'photo']


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Rule)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Service)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Experience)
admin.site.register(GroupReservation)
admin.site.register(InterestService)
admin.site.register(InterestServiceProperty)
admin.site.register(Message)
admin.site.register(StudentAnnouncement)
admin.site.register(UserValoration)
admin.site.register(PropertyValoration)









