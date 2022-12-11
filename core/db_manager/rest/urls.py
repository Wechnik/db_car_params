from db_manager.rest.view import VehicleViewREST
from django.urls.conf import path
from rest_framework.authtoken import views

urlpatterns = [
    path('api/v1/auth/', views.obtain_auth_token, name='rest_auth'),
    path('api/v1/vehicle/', VehicleViewREST.as_view(), name='rest_post_vehicle'),
]
