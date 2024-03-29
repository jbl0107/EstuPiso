from django.urls import path
from apis.api_users.api import (
    user_api_view, user_detail_api_view, user_valoration_received_api_view, user_valoration_done_to_users_api_view,
    get_user_type)

from apis.api_students.api import (
    student_api_view, student_detail_api_view, student_valoration_done_to_properties_api_view, student_verify_password, 
    student_profile_change_password, student_photo_update)

from apis.api_owners.api import (
    owner_api_view, owner_detail_api_view, owner_properties_api_view, owner_public_detail_api_view, owner_student_detail_api_view,
    owner_verify_password, owner_profile_change_password, owner_photo_update)

from apis.api_rules.api import rule_api_view, rule_detail_api_view

from apis.api_photos.api import (
    photo_api_view, photo_detail_api_view, photo_owner_detail_api_view)

from apis.api_services.api import service_api_view, service_detail_api_view

from apis.api_properties.api import (
    property_api_view, property_detail_api_view, property_rules_api_view, property_photos_api_view, 
    property_services_api_view, property_valorations_api_view, property_types)

from apis.api_messages.api import (
    message_api_view, message_detail_api_view, message_user_api_view, message_user_conversation_api_view)

from apis.api_valoration.api import (
    valoration_user_api_view, valoration_user_detail_api_view, valoration_property_api_view, valoration_property_detail_api_view)

from apis.api_groupReservations.api import (
    groupReservation_api_view, groupReservation_detail_api_view, groupReservation_student_api_view)

from apis.api_experiences.api import experience_api_view, experience_detail_api_view, experience_student_api_view

from apis.api_interestServices.api import (
    interestService_api_view, interestService_detail_api_view)

from apis.api_interestServicesProperty.api import (
    interestServiceProperty_api_view, interestServiceProperty_detail_api_view, interestServiceProperty_property_api_view)

from apis.api_studentAnnouncements.api import (
    studentAnnouncement_api_view, studentAnnouncement_detail_api_view, studentAnnouncement_student_api_view)


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import LogoutView


urlpatterns = [

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #devuelve token de acceso y token de refresco
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='token_logout'),

    path('users/', user_api_view, name='user_api'),
    path('users/<int:id>', user_detail_api_view, name='user_detail_api'),
    path('users/<int:id>/valorations/received', user_valoration_received_api_view, name='user_valorations_received_api'),
    path('users/<int:id>/valorations/done/users', user_valoration_done_to_users_api_view, name='user_valorations_done_to_users_api'),
    path('users/<int:id>/type', get_user_type, name='user_type_api'),

    path('students/', student_api_view, name='student_api'),
    path('students/<int:id>', student_detail_api_view, name='student_detail_api'),
    path('students/<int:id>/valorations/done/properties/', student_valoration_done_to_properties_api_view, name='student_valorations_done_to_properties_api'),
    path('students/verify-pass', student_verify_password, name='student_verify_pass_api'),
    path('students/profile-pass-change', student_profile_change_password, name='student_profile_pass_change'),
    path('students/photo-update/<int:id>', student_photo_update, name='student_photo_update'),

    path('owners/', owner_api_view, name='owner_api'),
    path('owners/<int:id>', owner_detail_api_view, name='owner_detail_api'),
    path('owners/<int:id>/properties', owner_properties_api_view, name='owner_properties_api'),
    path('owners/<int:id>/public', owner_public_detail_api_view, name='owner_public_detail_api'),
    path('owners/<int:id>/student', owner_student_detail_api_view, name='owner_student_detail_api'),
    path('owners/verify-pass', owner_verify_password, name='owner_verify_pass_api'),
    path('owners/profile-pass-change', owner_profile_change_password, name='owner_profile_pass_change'),
    path('owners/photo-update/<int:id>', owner_photo_update, name='owner_photo_update'),
    

    path('rules/', rule_api_view, name='rule_api'),
    path('rules/<int:id>', rule_detail_api_view, name='rule_detail_api'),

    path('photos/', photo_api_view, name='photo_api'),
    path('photos/<int:id>', photo_detail_api_view, name='photo_detail_api'), 
    path('photos/owner/<int:id>', photo_owner_detail_api_view, name='photo_owner_detail_api'), 


    path('services/', service_api_view, name='service_api'),
    path('services/<int:id>', service_detail_api_view, name='service_detail_api'),    

    path('properties/', property_api_view, name='property_api'),
    path('properties/<int:id>', property_detail_api_view, name='property_detail_api'),      
    path('properties/<int:id>/rules', property_rules_api_view, name='property_rules_api'),
    path('properties/<int:id>/photos', property_photos_api_view, name='property_photos_api'),
    path('properties/<int:id>/services', property_services_api_view, name='property_serviceS_api'),
    path('properties/<int:id>/valorations', property_valorations_api_view, name='property_valorations_api'),
    path('properties/types', property_types, name='property_types'),
    


    path('messages/', message_api_view, name='message_api'),
    path('messages/<int:id>', message_detail_api_view, name='message_detail_api'),   
    path('messages/user/<int:id_user>', message_user_api_view, name='message_user_api'),
    path('messages/<int:id_user1>/<int:id_user2>', message_user_conversation_api_view, name='message_user_conversation_api'),

    path('valorations/users/', valoration_user_api_view, name='valoration_user_api'),
    path('valorations/users/<int:id>', valoration_user_detail_api_view, name='valoration_user_detail_api'),
    path('valorations/properties/', valoration_property_api_view, name='valoration_property_api'),
    path('valorations/properties/<int:id>', valoration_property_detail_api_view, name='valoration_property_detail_api'),  

    path('groupReservations/', groupReservation_api_view, name='groupReservation_api'),
    path('groupReservations/<int:id>', groupReservation_detail_api_view, name='groupReservation_detail_api'),
    path('groupReservations/student/<int:id>', groupReservation_student_api_view, name='groupReservation_student_api'),

    path('experiences/', experience_api_view, name='experience_api'),
    path('experiences/<int:id>', experience_detail_api_view, name='experience_detail_api'),
    path('experiences/student/<int:id>', experience_student_api_view, name='experience_student_api'),

    path('interestServices/', interestService_api_view, name='interestService_api'),
    path('interestServices/<int:id>', interestService_detail_api_view, name='interestService_detail_api'),

    path('interestServicesProperty/', interestServiceProperty_api_view, name='interestServiceProperty_api'),
    path('interestServicesProperty/<int:id>', interestServiceProperty_detail_api_view, name='interestServiceProperty_detail_api'),
    path('interestServicesProperty/property/<int:id>', interestServiceProperty_property_api_view, name='interestServicesProperty_property_api'),

    path('studentAnnouncements/', studentAnnouncement_api_view, name='studentAnnouncement_api'),
    path('studentAnnouncements/<int:id>', studentAnnouncement_detail_api_view, name='studentAnnouncement_detail_api'),
    path('studentAnnouncements/student/<int:id>', studentAnnouncement_student_api_view, name='studentAnnouncement_student_api'),



]
