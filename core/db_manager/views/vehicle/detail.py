__all__ = ['VehicleDetailView']

from db_manager.models import Vehicle
from db_manager.views.detail import BaseVehicleDetailView


class VehicleDetailView(BaseVehicleDetailView):
    template_name = 'all_car/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        vehicle = Vehicle.objects.filter(parent=context['vehicle'].id)
        context['parent'] = context['vehicle']
        if vehicle:
            context['vehicle'] = list(vehicle)
        else:
            context['vehicle'] = [context['vehicle']]
            context['isBaseConfiguration'] = 'True'

        return context
