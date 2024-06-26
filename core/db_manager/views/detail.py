__all__ = ['BaseVehicleDetailView', 'BrandDetailView', 'ModelDetailView']

from db_manager.models import Vehicle
from django.views.generic import DetailView

from db_manager.views.abstract import BaseLoginRequiredMixin


class BaseVehicleDetailView(BaseLoginRequiredMixin, DetailView):
    model = Vehicle
    template_name = 'crud/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(context["vehicle"])
        return context


class BrandDetailView(BaseVehicleDetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = '_brand'
        return context


class ModelDetailView(BaseVehicleDetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = '_model'
        return context
