from django.views.generic.edit import CreateView

from db_manager.models import Vehicle

__all__ = ['VehicleCreateView']


class VehicleCreateView(CreateView):
    model = Vehicle
    queryset = Vehicle.objects.all()
    template_name = 'crud/create.html'
    fields = '__all__'
