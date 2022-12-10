__all__ = ['VehicleDetailView']

from db_manager.models import Vehicle
from db_manager.views.detail import BaseVehicleDetailView


class VehicleDetailView(BaseVehicleDetailView):
    template_name = 'all_car/detail.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.preferred_config = None

    def get(self, request, *args, **kwargs):
        self.preferred_config = kwargs.get('cfg_pk')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        generation = context['vehicle']
        context['generation'] = generation

        config_list = list(Vehicle.objects.filter(parent=context['vehicle'].id))
        if not config_list:
            current_config = context['vehicle']
            current_config.name = 'Базовая комплектация'
            config_list = [current_config]

        if not self.preferred_config:
            config_list[0].selected = True
        else:
            for config in config_list:
                if self.preferred_config == config.id:
                    config.selected = True
                    break
            else:
                config_list[0].selected = True

        context['config_list'] = config_list

        return context
