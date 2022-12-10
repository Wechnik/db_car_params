from db_manager.views.detail import BaseVehicleDetailView


class ConfigurationDetailView(BaseVehicleDetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = '_configuration'
        return context
