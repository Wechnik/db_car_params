from django.urls import reverse
from django.views.generic import CreateView

from db_manager.forms.configuration import ConfigurationForm
from db_manager.models import Vehicle
from db_manager.views.abstract import BaseLoginRequiredMixin


class ConfigurationCreateView(BaseLoginRequiredMixin, CreateView):
    form_class = ConfigurationForm
    template_name = 'crud/create.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generation = None

    def post(self, request, *args, **kwargs):
        self.generation = Vehicle.objects.get(id=kwargs.get('pk'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance._type = Vehicle.Type.CONFIGURATION.value
        form.instance.parent = self.generation
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.parent.id, 'cfg_pk': self.object.id})
