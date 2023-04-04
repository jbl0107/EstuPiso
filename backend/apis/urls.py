from django.urls import path
from apis.api_users.api import user_api_view, user_detail_api_view
from apis.api_students.api import student_api_view, student_detail_api_view
from apis.api_owners.api import owner_api_view, owner_detail_api_view, owner_properties_api_view
from apis.api_rules.api import rule_api_view, rule_detail_api_view
from apis.api_photos.api import photo_api_view, photo_detail_api_view
from apis.api_services.api import service_api_view, service_detail_api_view
from apis.api_properties.api import property_api_view, property_detail_api_view, property_rules_api_view, property_photos_api_view, property_services_api_view
from apis.api_messages.api import message_api_view, message_detail_api_view, message_user_api_view, message_user_conversation_api_view

urlpatterns = [
    path('users/', user_api_view, name='user_api'),
    path('users/<int:id>', user_detail_api_view, name='user_detail_api'),
    
    path('students/', student_api_view, name='student_api'),
    path('students/<int:id>', student_detail_api_view, name='student_detail_api'),

    path('owners/', owner_api_view, name='owner_api'),
    path('owners/<int:id>', owner_detail_api_view, name='owner_detail_api'),
    path('owners/<int:id>/properties', owner_properties_api_view, name='owner_properties_api'),

    path('rules/', rule_api_view, name='rule_api'),
    path('rules/<int:id>', rule_detail_api_view, name='rule_detail_api'),

    path('photos/', photo_api_view, name='photo_api'),
    path('photos/<int:id>', photo_detail_api_view, name='photo_detail_api'),   

    path('services/', service_api_view, name='service_api'),
    path('services/<int:id>', service_detail_api_view, name='service_detail_api'),    

    path('properties/', property_api_view, name='property_api'),
    path('properties/<int:id>', property_detail_api_view, name='property_detail_api'),      
    path('properties/<int:id>/rules', property_rules_api_view, name='property_rules_api'),
    path('properties/<int:id>/photos', property_photos_api_view, name='property_photos_api'),
    path('properties/<int:id>/services', property_services_api_view, name='property_serviceS_api'),

    path('messages/', message_api_view, name='message_api'),
    path('messages/<int:id>', message_detail_api_view, name='message_detail_api'),   
    path('messages/user/<int:id_user>', message_user_api_view, name='message_user_api'),
    path('messages/<int:id_user1>/<int:id_user2>', message_user_conversation_api_view, name='message_user_conversation_api')

]
