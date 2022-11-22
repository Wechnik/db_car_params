from db_manager.models import Vehicle
from django.urls import reverse_lazy
from django.views.generic import DeleteView

__all__ = ['VehicleDeleteView']


class BaseVehicleDeleteView(DeleteView):
    model = Vehicle
    template_name = 'crud/delete.html'


class VehicleDeleteView(BaseVehicleDeleteView):
    success_url = reverse_lazy('index')


class BrandDeleteView(BaseVehicleDeleteView):
    success_url = reverse_lazy('brand')


class ModelDeleteView(BaseVehicleDeleteView):
    success_url = reverse_lazy('model')


class GenerationDeleteView(BaseVehicleDeleteView):
    success_url = reverse_lazy('generation')


class RestylingDeleteView(BaseVehicleDeleteView):
    success_url = reverse_lazy('restyling')


class ConfigurationDeleteView(BaseVehicleDeleteView):
    success_url = reverse_lazy('configuration')
