from django.urls import reverse
from django.views.generic import UpdateView

from db_manager.forms.configuration import ConfigurationForm
from db_manager.models import Vehicle
from db_manager.views.abstract import BaseLoginRequiredMixin


class ConfigurationUpdateView(BaseLoginRequiredMixin, UpdateView):
    form_class = ConfigurationForm
    template_name = 'crud/create.html'
    queryset = Vehicle.objects.all()

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.parent.id, 'cfg_pk': self.object.id})
