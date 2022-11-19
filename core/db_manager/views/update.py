from django.views.generic.edit import UpdateView

from db_manager.models import Vehicle

__all__ = ['VehicleUpdateView']


class VehicleUpdateView(UpdateView):
    model = Vehicle
    template_name = 'crud/update.html'
    fields = '__all__'
