__all__ = ['BaseVehicleUpdateView']

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.edit import UpdateView

from db_manager.models import Vehicle
from db_manager.views.abstract import BaseLoginRequiredMixin
from db_manager.forms.crud_forms import (
    BaseVehicleForm,
    BrandForm,
    GenerationForm,
    ModelForm
)
from db_manager.forms.configuration import ConfigurationForm


class BaseVehicleUpdateView(BaseLoginRequiredMixin, UpdateView):
    model = Vehicle
    queryset = Vehicle.objects.all()
    template_name = 'crud/create.html'
    form_class = BaseVehicleForm

    _url = NotImplemented
    _name = NotImplemented

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактировать {self._name}'
        return context

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return redirect(self._url)


class BrandUpdateView(BaseVehicleUpdateView):
    form_class = BrandForm
    _url = 'brand'
    _name = 'бренд'


class ModelUpdateView(BaseVehicleUpdateView):
    form_class = ModelForm
    _url = 'model'
    _name = 'модель'


class GenerationUpdateView(BaseVehicleUpdateView):
    form_class = GenerationForm
    _url = 'generation'
    _name = 'поколение'


class ConfigurationUpdateView(BaseLoginRequiredMixin, UpdateView):
    form_class = ConfigurationForm
    template_name = 'crud/create.html'
    queryset = Vehicle.objects.all()

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.parent.id, 'cfg_pk': self.object.id})

