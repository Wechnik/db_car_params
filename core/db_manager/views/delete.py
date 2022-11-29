from db_manager.models import Vehicle
from django.urls import reverse_lazy
from django.views.generic import DeleteView

__all__ = ['VehicleDeleteView']


class BaseVehicleDeleteView(DeleteView):
    model = Vehicle
    template_name = 'crud/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление авто'
        return context


class VehicleDeleteView(BaseVehicleDeleteView):
    success_url = reverse_lazy('index')


class BrandDeleteView(BaseVehicleDeleteView):
    success_url = reverse_lazy('brand')


class ModelDeleteView(BaseVehicleDeleteView):
    success_url = reverse_lazy('model')


class GenerationDeleteView(BaseVehicleDeleteView):
    success_url = reverse_lazy('generation')


class ConfigurationDeleteView(BaseVehicleDeleteView):
    success_url = reverse_lazy('configuration')
