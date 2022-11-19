from django.urls import reverse_lazy
from django.views.generic import DeleteView

from db_manager.models import Vehicle

__all__ = ['VehicleDeleteView']


class VehicleDeleteView(DeleteView):
    model = Vehicle
    template_name = 'crud/delete.html'
    success_url = reverse_lazy('')
