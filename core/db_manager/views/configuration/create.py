from django.urls import reverse
from django.views.generic import CreateView

from db_manager.forms.configuration import ConfigurationForm
from db_manager.models import Vehicle
from db_manager.views.abstract import BaseLoginRequiredMixin


class ConfigurationCreateView(BaseLoginRequiredMixin, CreateView):
    form_class = ConfigurationForm
    template_name = 'configuration/create.html'

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['parent'] = Vehicle.objects.get(id=self.kwargs['pk'])

        try:
            form_kwargs['initial_attributes'] = Vehicle.objects.filter(parent=self.kwargs['pk']).order_by('id')[0]\
                .get_hierarchy_attributes
        except IndexError:
            form_kwargs['initial_attributes'] = None

        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        gen = Vehicle.objects.get(id=self.kwargs['pk'])
        context['generation'] = gen

        # Комплектации будут отсортированы по возрастанию даты начала выпуска.
        # Комплектации, у которых даты производства совпадают, будут отсортированы по дате конца выпуска.
        config_list = Vehicle.objects.filter(parent=gen.id).order_by('id')

        # Нужна для отображения списка доступных комплектаций и информации о самих комплектациях.
        context['config_list'] = config_list

        context['title'] = gen

        context['select_plus'] = True

        return context

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
        return reverse('edit_configuration', kwargs={'pk': self.object.id})
