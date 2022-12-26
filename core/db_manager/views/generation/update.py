from django.urls import reverse
from django.views.generic import UpdateView

from db_manager.forms.generation import GenerationForm
from db_manager.models import Vehicle
from db_manager.views.abstract import BaseLoginRequiredMixin


class GenerationUpdateView(BaseLoginRequiredMixin, UpdateView):
    form_class = GenerationForm
    template_name = 'crud/create.html'
    queryset = Vehicle.objects.all()

    def get_success_url(self):
        return reverse('detail_generation', kwargs={'pk': self.object.id})
