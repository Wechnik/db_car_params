from db_manager.views import IndexView, VehicleCreateView, VehicleDeleteView, VehicleDetailView, VehicleUpdateView
from db_manager.views.create import (
    BrandCreateView,
    ConfigurationCreateView,
    GenerationCreateView,
    ModelCreateView,
    RestylingCreateView
)
from db_manager.views.delete import (
    BrandDeleteView,
    ConfigurationDeleteView,
    GenerationDeleteView,
    ModelDeleteView,
    RestylingDeleteView
)
from db_manager.views.detail import (
    BrandDetailView,
    ConfigurationDetailView,
    GenerationDetailView,
    ModelDetailView,
    RestylingDetailView
)
from db_manager.views.index import BrandView, ConfigurationView, GenerationView, ModelView, RestylingView
from db_manager.views.update import (
    BrandUpdateView,
    ConfigurationUpdateView,
    GenerationUpdateView,
    ModelUpdateView,
    RestylingUpdateView
)
from django.urls.conf import include, path

crud_vehicle = [
    path('new/', VehicleCreateView.as_view(), name='create'),
    path('<int:pk>/', VehicleDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', VehicleUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', VehicleDeleteView.as_view(), name='delete'),
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

crud_restyling = [
    path('', RestylingView.as_view(), name='restyling'),
    path('new/', RestylingCreateView.as_view(), name='create_restyling'),
    path('<int:pk>/', RestylingDetailView.as_view(), name='detail_restyling'),
    path('<int:pk>/edit/', RestylingUpdateView.as_view(), name='edit_restyling'),
    path('<int:pk>/delete/', RestylingDeleteView.as_view(), name='delete_restyling'),
]

crud_configuration = [
    path('', ConfigurationView.as_view(), name='configuration'),
    path('new/', ConfigurationCreateView.as_view(), name='create_configuration'),
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
    path('restyling/', include(crud_restyling)),
    path('configuration/', include(crud_configuration)),
]
