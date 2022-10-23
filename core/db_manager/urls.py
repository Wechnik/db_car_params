from django.urls.conf import path, include

from db_manager import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('django.contrib.auth.urls')),
]
