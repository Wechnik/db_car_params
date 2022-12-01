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


class BaseVehicleUpdateView(UpdateView):
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


class BrandUpdateView(BaseVehicleUpdateView):
    form_class = BrandForm
    _url = 'brand'
    _name = 'бренд'

    def form_valid(self, form):
        form.instance._type = 0
        return super().form_valid(form)


class ModelUpdateView(BaseVehicleUpdateView):
    form_class = ModelForm
    _url = 'model'
    _name = 'модель'

    def form_valid(self, form):
        form.instance._type = 1
        return super().form_valid(form)


class GenerationUpdateView(BaseVehicleUpdateView):
    form_class = GenerationForm
    _url = 'generation'
    _name = 'поколение'

    def form_valid(self, form):
        form.instance._type = 2
        return super().form_valid(form)


class ConfigurationUpdateView(BaseVehicleUpdateView):
    form_class = ConfigurationForm
    _url = 'configuration'
    _name = 'комплектацию'

    def form_valid(self, form):
        form.instance._type = 3
        return super().form_valid(form)
