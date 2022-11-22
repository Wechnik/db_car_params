from django.views.generic.edit import CreateView

from db_manager.forms.crud_forms import VehicleForm
from db_manager.models import Vehicle

__all__ = ['VehicleCreateView']


class VehicleCreateView(CreateView):
    model = Vehicle
    queryset = Vehicle.objects.all()
    template_name = 'crud/create.html'
    form_class = VehicleForm
