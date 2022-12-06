from django.shortcuts import redirect

from db_manager.forms.crud_forms import (
    BaseVehicleForm,
    BrandForm,
    ConfigurationForm,
    GenerationForm,
    ModelForm,
    VehicleForm
)
from db_manager.models import Vehicle
from django.views.generic.edit import UpdateView

__all__ = ['VehicleUpdateView']

from db_manager.views.abstract import BaseLoginRequiredMixin


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


class VehicleUpdateView(BaseVehicleUpdateView):
    form_class = VehicleForm
    template_name = 'all_car/update.html'
    _url = 'index'
    _name = 'автомобиль'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = Vehicle.objects.filter(parent=context['vehicle'].id)
        if vehicle:
            context['vehicle'] = list(vehicle)
        else:
            context['vehicle'] = [context['vehicle']]
            context['isBaseConfiguration'] = True
        context['title'] = f'Редактировать {self._name}'
        return context


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


class ConfigurationUpdateView(BaseVehicleUpdateView):
    form_class = ConfigurationForm
    _url = 'configuration'
    _name = 'комплектацию'
