from django.urls.conf import include, path

from db_manager.views import IndexView, VehicleDetailView
from db_manager.views.configuration.create import ConfigurationCreateView
from db_manager.views.configuration.delete import ConfigurationDeleteView
from db_manager.views.configuration.detail import ConfigurationDetailView
from db_manager.views.configuration.update import ConfigurationUpdateView
from db_manager.views.create import BrandCreateView, ModelCreateView
from db_manager.views.delete import (BrandDeleteView, GenerationDeleteView,
                                     ModelDeleteView)
from db_manager.views.detail import BrandDetailView, ModelDetailView
from db_manager.views.generation.copy import CopyView
from db_manager.views.generation.create import GenerationCreateView
from db_manager.views.generation.detail import GenerationDetailView
from db_manager.views.generation.update import GenerationUpdateView
from db_manager.views.index import (BrandView, GenerationView, ModelView,
                                    VehiclesAlt)
from db_manager.views.params.create import (OilTypeCreateView,
                                            OilViscosityCreateView,
                                            TireDiameterCreateView,
                                            TireInchHeightCreateView,
                                            TireInchWidthCreateView,
                                            TireMetricProfileCreateView,
                                            TireMetricWidthCreateView,
                                            WheelCHDiameterCreateView,
                                            WheelDepartureCreateView,
                                            WheelDiameterCreateView,
                                            WheelDrillingCreateView,
                                            WheelWidthCreateView,
                                            WipersLengthCreateView, YearCreateView)
from db_manager.views.params.delete import (OilTypeDeleteView,
                                            OilViscosityDeleteView,
                                            TireDiameterDeleteView,
                                            TireInchHeightDeleteView,
                                            TireInchWidthDeleteView,
                                            TireMetricProfileDeleteView,
                                            TireMetricWidthDeleteView,
                                            WheelCHDiameterDeleteView,
                                            WheelDepartureDeleteView,
                                            WheelDiameterDeleteView,
                                            WheelDrillingDeleteView,
                                            WheelWidthDeleteView,
                                            WipersLengthDeleteView, YearDeleteView)
from db_manager.views.params.index import (OilTypeView, OilViscosityView,
                                           TireDiameterView,
                                           TireInchHeightView,
                                           TireInchWidthView,
                                           TireMetricProfileView,
                                           TireMetricWidthView,
                                           WheelCHDiameterView,
                                           WheelDepartureView,
                                           WheelDiameterView,
                                           WheelDrillingView, WheelWidthView,
                                           WipersLengthView, YearView)
from db_manager.views.params.update import (OilTypeUpdateView,
                                            OilViscosityUpdateView,
                                            TireDiameterUpdateView,
                                            TireInchHeightUpdateView,
                                            TireInchWidthUpdateView,
                                            TireMetricProfileUpdateView,
                                            TireMetricWidthUpdateView,
                                            WheelCHDiameterUpdateView,
                                            WheelDepartureUpdateView,
                                            WheelDiameterUpdateView,
                                            WheelDrillingUpdateView,
                                            WheelWidthUpdateView,
                                            WipersLengthUpdateView, YearUpdateView)
from db_manager.views.update import BrandUpdateView, ModelUpdateView

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
    path('<int:pk>/copy/', CopyView.as_view(), name='copy_generation'),
]

crud_configuration = [
    path('<int:pk>/', ConfigurationDetailView.as_view(), name='detail_configuration'),
    path('<int:pk>/edit/', ConfigurationUpdateView.as_view(), name='edit_configuration'),
    path('<int:pk>/delete/', ConfigurationDeleteView.as_view(), name='delete_configuration'),
]


# Params value

crud_tire_diameter = [
    path('', TireDiameterView.as_view(), name='tire_diameter'),
    path('new/', TireDiameterCreateView.as_view(), name='create_tire_diameter'),
    path('<int:pk>/edit/', TireDiameterUpdateView.as_view(), name='edit_tire_diameter'),
    path('<int:pk>/delete/', TireDiameterDeleteView.as_view(), name='delete_tire_diameter'),
]


crud_tire_metric_width = [
    path('', TireMetricWidthView.as_view(), name='tire_metric_width'),
    path('new/', TireMetricWidthCreateView.as_view(), name='create_tire_metric_width'),
    path('<int:pk>/edit/', TireMetricWidthUpdateView.as_view(), name='edit_tire_metric_width'),
    path('<int:pk>/delete/', TireMetricWidthDeleteView.as_view(), name='delete_tire_metric_width'),
]


crud_tire_metric_profile = [
    path('', TireMetricProfileView.as_view(), name='tire_metric_profile'),
    path('new/', TireMetricProfileCreateView.as_view(), name='create_tire_metric_profile'),
    path('<int:pk>/edit/', TireMetricProfileUpdateView.as_view(), name='edit_tire_metric_profile'),
    path('<int:pk>/delete/', TireMetricProfileDeleteView.as_view(), name='delete_tire_metric_profile'),
]


crud_tire_inch_width = [
    path('', TireInchWidthView.as_view(), name='tire_inch_width'),
    path('new/', TireInchWidthCreateView.as_view(), name='create_tire_inch_width'),
    path('<int:pk>/edit/', TireInchWidthUpdateView.as_view(), name='edit_tire_inch_width'),
    path('<int:pk>/delete/', TireInchWidthDeleteView.as_view(), name='delete_tire_inch_width'),
]


crud_tire_inch_height = [
    path('', TireInchHeightView.as_view(), name='tire_inch_height'),
    path('new/', TireInchHeightCreateView.as_view(), name='create_tire_inch_height'),
    path('<int:pk>/edit/', TireInchHeightUpdateView.as_view(), name='edit_tire_inch_height'),
    path('<int:pk>/delete/', TireInchHeightDeleteView.as_view(), name='delete_tire_inch_height'),
]


crud_wheel_width = [
    path('', WheelWidthView.as_view(), name='wheel_width'),
    path('new/', WheelWidthCreateView.as_view(), name='create_wheel_width'),
    path('<int:pk>/edit/', WheelWidthUpdateView.as_view(), name='edit_wheel_width'),
    path('<int:pk>/delete/', WheelWidthDeleteView.as_view(), name='delete_wheel_width'),
]


crud_wheel_diameter = [
    path('', WheelDiameterView.as_view(), name='wheel_diameter'),
    path('new/', WheelDiameterCreateView.as_view(), name='create_wheel_diameter'),
    path('<int:pk>/edit/', WheelDiameterUpdateView.as_view(), name='edit_wheel_diameter'),
    path('<int:pk>/delete/', WheelDiameterDeleteView.as_view(), name='delete_wheel_diameter'),
]


crud_wheel_drilling = [
    path('', WheelDrillingView.as_view(), name='wheel_drilling'),
    path('new/', WheelDrillingCreateView.as_view(), name='create_wheel_drilling'),
    path('<int:pk>/edit/', WheelDrillingUpdateView.as_view(), name='edit_wheel_drilling'),
    path('<int:pk>/delete/', WheelDrillingDeleteView.as_view(), name='delete_wheel_drilling'),
]


crud_wheel_departure = [
    path('', WheelDepartureView.as_view(), name='wheel_departure'),
    path('new/', WheelDepartureCreateView.as_view(), name='create_wheel_departure'),
    path('<int:pk>/edit/', WheelDepartureUpdateView.as_view(), name='edit_wheel_departure'),
    path('<int:pk>/delete/', WheelDepartureDeleteView.as_view(), name='delete_wheel_departure'),
]


crud_wheel_ch_diameter = [
    path('', WheelCHDiameterView.as_view(), name='wheel_ch_diameter'),
    path('new/', WheelCHDiameterCreateView.as_view(), name='create_wheel_ch_diameter'),
    path('<int:pk>/edit/', WheelCHDiameterUpdateView.as_view(), name='edit_wheel_ch_diameter'),
    path('<int:pk>/delete/', WheelCHDiameterDeleteView.as_view(), name='delete_wheel_ch_diameter'),
]


crud_oil_type = [
    path('', OilTypeView.as_view(), name='oil_type'),
    path('new/', OilTypeCreateView.as_view(), name='create_oil_type'),
    path('<int:pk>/edit/', OilTypeUpdateView.as_view(), name='edit_oil_type'),
    path('<int:pk>/delete/', OilTypeDeleteView.as_view(), name='delete_oil_type'),
]


crud_oil_viscosity = [
    path('', OilViscosityView.as_view(), name='oil_viscosity'),
    path('new/', OilViscosityCreateView.as_view(), name='create_oil_viscosity'),
    path('<int:pk>/edit/', OilViscosityUpdateView.as_view(), name='edit_oil_viscosity'),
    path('<int:pk>/delete/', OilViscosityDeleteView.as_view(), name='delete_oil_viscosity'),
]

crud_wipers_length = [
    path('', WipersLengthView.as_view(), name='wipers_length'),
    path('new/', WipersLengthCreateView.as_view(), name='create_wipers_length'),
    path('<int:pk>/edit/', WipersLengthUpdateView.as_view(), name='edit_wipers_length'),
    path('<int:pk>/delete/', WipersLengthDeleteView.as_view(), name='delete_wipers_length'),
]

crud_year = [
    path('', YearView.as_view(), name='year'),
    path('new/', YearCreateView.as_view(), name='create_year'),
    path('<int:pk>/edit/', YearUpdateView.as_view(), name='edit_year'),
    path('<int:pk>/delete/', YearDeleteView.as_view(), name='delete_year'),
]

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('alt/', VehiclesAlt.as_view(), name='index_alt'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('vehicle/', include(crud_vehicle)),
    path('brand/', include(crud_brand)),
    path('model/', include(crud_model)),
    path('generation/', include(crud_generation)),
    path('configuration/', include(crud_configuration)),

    path('tire_diameter/', include(crud_tire_diameter)),
    path('tire_metric_width/', include(crud_tire_metric_width)),
    path('tire_metric_profile/', include(crud_tire_metric_profile)),
    path('tire_inch_width/', include(crud_tire_inch_width)),
    path('tire_inch_height/', include(crud_tire_inch_height)),

    path('wheel_width/', include(crud_wheel_width)),
    path('wheel_diameter/', include(crud_wheel_diameter)),
    path('wheel_drilling/', include(crud_wheel_drilling)),
    path('wheel_departure/', include(crud_wheel_departure)),
    path('wheel_ch_diameter/', include(crud_wheel_ch_diameter)),

    path('oil_type/', include(crud_oil_type)),
    path('oil_viscosity/', include(crud_oil_viscosity)),

    path('wipers_length/', include(crud_wipers_length)),

    path('year/', include(crud_year)),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
