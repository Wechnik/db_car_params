from django.urls.conf import path

from db_manager import views

urlpatterns = [
    path('', views.index, name='index'),
]
