from django.views.generic import DetailView

from db_manager.models import Vehicle

__all__ = ['VehicleDetailView']


class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'crud/detail.html'
