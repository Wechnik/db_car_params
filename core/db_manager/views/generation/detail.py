from db_manager.views.detail import BaseVehicleDetailView


class GenerationDetailView(BaseVehicleDetailView):
    template_name = 'generation/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = '_generation'
        return context
