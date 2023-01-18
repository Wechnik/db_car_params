from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View

from db_manager.models import Vehicle
from db_manager.views.abstract import BaseLoginRequiredMixin


class CopyView(BaseLoginRequiredMixin, View):
    """Представление для копирования поколения и его комплектаций."""

    def get(self, request, pk):
        Vehicle.objects.get(id=pk).copy(first_level_name_suffix=' (Копия)')
        return HttpResponseRedirect(reverse('index'))
