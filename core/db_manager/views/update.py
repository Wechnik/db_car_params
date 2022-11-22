from django.views.generic.edit import UpdateView

from db_manager.forms.crud_forms import VehicleForm
from db_manager.models import Vehicle

__all__ = ['VehicleUpdateView']


class VehicleUpdateView(UpdateView):
    model = Vehicle
    template_name = 'crud/update.html'
    form_class = VehicleForm
