from django.urls import path
from apis.api_users.api import user_api_view, user_detail_api_view
from apis.api_students.api import student_api_view, student_detail_api_view
from apis.api_owners.api import owner_api_view, owner_detail_api_view

urlpatterns = [
    path('users/', user_api_view, name='user_api'),
    path('users/<int:id>', user_detail_api_view, name='user_detail_api'),
    path('students/', student_api_view, name='student_api'),
    path('students/<int:id>', student_detail_api_view, name='student_detail_api'),
    path('owners/', owner_api_view, name='owner_api'),
    path('owners/<int:id>', owner_detail_api_view, name='owner_detail_api')

]
