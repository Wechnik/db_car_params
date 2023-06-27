from django.views.generic import ListView

from db_manager.forms.core import Sorter
from db_manager.models import ParamsValue
from db_manager.views import BaseLoginRequiredMixin


class WheelDependenciesListView(BaseLoginRequiredMixin, ListView):
    template_name = 'dependencies/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['root_params'] = Sorter.sort_drilling(self.get_queryset().filter(type=ParamsValue.Type.WHEEL_DRILLING))
        context['level_1_params'] = Sorter.sort_diameter(self.get_queryset().filter(type=ParamsValue.Type.WHEEL_DIAMETER))
        context['level_2_params'] = Sorter.sort_number(self.get_queryset().filter(type=ParamsValue.Type.WHEEL_WIDTH))

        return context

    def get_queryset(self):
        return ParamsValue.objects.prefetch_related('child')
