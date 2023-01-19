from db_manager.forms.generation import GenerationForm
from db_manager.models import Vehicle
from db_manager.views.abstract import BaseLoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView


class GenerationCreateView(BaseLoginRequiredMixin, CreateView):
    form_class = GenerationForm
    template_name = 'crud/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Создание поколения'
        return context

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parent = None

    # def post(self, request, *args, **kwargs):
    #     self.parent = Vehicle.objects.get(id=kwargs.get('pk'))
    #     return super().post(request, *args, **kwargs)

    # def form_valid(self, form):
    #     form.instance._type = Vehicle.Type.GENERATION.value
    #     form.instance.parent = self.parent
    #     return super().form_valid(form)

    def form_valid(self, form):
        form.instance._type = Vehicle.Type.GENERATION.value
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.id})
