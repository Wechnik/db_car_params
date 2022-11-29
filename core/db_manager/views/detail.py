from db_manager.models import Vehicle
from django.views.generic import DetailView

__all__ = ['VehicleDetailView']


class BaseVehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'crud/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Просмотр - {context["vehicle"]}'
        return context


class VehicleDetailView(BaseVehicleDetailView):
    template_name = 'crud/detail_vehicle.html'


class BrandDetailView(BaseVehicleDetailView):
    pass


class ModelDetailView(BaseVehicleDetailView):
    pass


class GenerationDetailView(BaseVehicleDetailView):
    pass


class ConfigurationDetailView(BaseVehicleDetailView):
    pass
