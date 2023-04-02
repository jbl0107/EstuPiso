from django.urls import path
from apis.api_users.api import user_api_view, user_detail_api_view


urlpatterns = [
    path('users/', user_api_view, name='user_api'),
    path('users/<int:id>', user_detail_api_view, name='user_detail_api'),

]
