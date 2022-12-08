__all__ = ['VehicleUpdateView']

from db_manager.forms.crud_forms import VehicleForm
from db_manager.models import Vehicle
from db_manager.views.update import BaseVehicleUpdateView


class VehicleUpdateView(BaseVehicleUpdateView):
    form_class = VehicleForm
    template_name = 'all_car/update.html'
    _url = 'index'
    _name = 'автомобиль'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        vehicle = Vehicle.objects.filter(parent=context['vehicle'].id)
        if vehicle:
            context['vehicle'] = list(vehicle)
        else:
            context['vehicle'] = [context['vehicle']]
            context['isBaseConfiguration'] = True

        context['title'] = f'Редактировать {self._name}'

        return context
