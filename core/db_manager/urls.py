from django.urls.conf import path, include

from db_manager.views import IndexView, VehicleCreateView, VehicleUpdateView, VehicleDetailView, VehicleDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('vehicle/new/', VehicleCreateView.as_view(), name='create'),
    path('vehicle/<int:pk>/', VehicleDetailView.as_view(), name='detail'),
    path('vehicle/<int:pk>/edit/', VehicleUpdateView.as_view(), name='edit'),
    path('vehicle/<int:pk>/delete/', VehicleDeleteView.as_view(), name='delete'),
]
