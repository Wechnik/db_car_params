from db_manager.models import Vehicle
from django.views.generic import DetailView

__all__ = ['VehicleDetailView']


class BaseVehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'crud/detail.html'


class VehicleDetailView(BaseVehicleDetailView):
    pass


class BrandDetailView(BaseVehicleDetailView):
    pass


class ModelDetailView(BaseVehicleDetailView):
    pass


class GenerationDetailView(BaseVehicleDetailView):
    pass


class RestylingDetailView(BaseVehicleDetailView):
    pass


class ConfigurationDetailView(BaseVehicleDetailView):
    pass
