from django.urls import reverse_lazy

from db_manager.views.delete import BaseVehicleDeleteView


class ConfigurationDeleteView(BaseVehicleDeleteView):
    success_url = reverse_lazy('configuration')
