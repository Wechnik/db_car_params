from db_manager.views import IndexView, VehicleDetailView
from db_manager.views.configuration.create import ConfigurationCreateView
from db_manager.views.configuration.delete import ConfigurationDeleteView
from db_manager.views.configuration.detail import ConfigurationDetailView
from db_manager.views.configuration.update import ConfigurationUpdateView
from db_manager.views.create import BrandCreateView, GenerationCreateView, ModelCreateView
from db_manager.views.delete import BrandDeleteView, GenerationDeleteView, ModelDeleteView
from db_manager.views.detail import BrandDetailView, GenerationDetailView, ModelDetailView
from db_manager.views.index import BrandView, GenerationView, ModelView
from db_manager.views.update import BrandUpdateView, GenerationUpdateView, ModelUpdateView
from django.urls.conf import include, path

crud_vehicle = [
    path('<int:pk>/', VehicleDetailView.as_view(), name='detail'),
    # FIXME: Пробросить config_id через сессию, чтобы не создавать доп. юрл?
    path('<int:pk>/configuration/<int:cfg_pk>/', VehicleDetailView.as_view(), name='detail'),
    path('<int:pk>/add-configuration/', ConfigurationCreateView.as_view(), name='add_configuration'),
]

crud_brand = [
    path('', BrandView.as_view(), name='brand'),
    path('new/', BrandCreateView.as_view(), name='create_brand'),
    path('<int:pk>/', BrandDetailView.as_view(), name='detail_brand'),
    path('<int:pk>/edit/', BrandUpdateView.as_view(), name='edit_brand'),
    path('<int:pk>/delete/', BrandDeleteView.as_view(), name='delete_brand'),
]

crud_model = [
    path('', ModelView.as_view(), name='model'),
    path('new/', ModelCreateView.as_view(), name='create_model'),
    path('<int:pk>/', ModelDetailView.as_view(), name='detail_model'),
    path('<int:pk>/edit/', ModelUpdateView.as_view(), name='edit_model'),
    path('<int:pk>/delete/', ModelDeleteView.as_view(), name='delete_model'),
]

crud_generation = [
    path('', GenerationView.as_view(), name='generation'),
    path('new/', GenerationCreateView.as_view(), name='create_generation'),
    path('<int:pk>/', GenerationDetailView.as_view(), name='detail_generation'),
    path('<int:pk>/edit/', GenerationUpdateView.as_view(), name='edit_generation'),
    path('<int:pk>/delete/', GenerationDeleteView.as_view(), name='delete_generation'),
]

crud_configuration = [
    path('<int:pk>/', ConfigurationDetailView.as_view(), name='detail_configuration'),
    path('<int:pk>/edit/', ConfigurationUpdateView.as_view(), name='edit_configuration'),
    path('<int:pk>/delete/', ConfigurationDeleteView.as_view(), name='delete_configuration'),
]


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('vehicle/', include(crud_vehicle)),
    path('brand/', include(crud_brand)),
    path('model/', include(crud_model)),
    path('generation/', include(crud_generation)),
    path('configuration/', include(crud_configuration)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
