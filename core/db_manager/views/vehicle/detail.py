__all__ = ['VehicleDetailView']

from db_manager.models import Vehicle
from db_manager.views.detail import BaseVehicleDetailView


class VehicleDetailView(BaseVehicleDetailView):
    template_name = 'all_car/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        generation = context['vehicle']
        context['generation'] = generation

        config_list = Vehicle.objects.filter(parent=context['vehicle'].id)
        if not config_list:
            current_config = context['vehicle']
            current_config.name = 'Базовая комплектация'
            config_list = [current_config]

        context['config_list'] = config_list

        return context
