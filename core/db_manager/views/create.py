from django.shortcuts import redirect

from db_manager.forms.crud_forms import (
    BaseVehicleForm,
    BrandForm,
    ConfigurationForm,
    GenerationForm,
    ModelForm,
    RestylingForm,
    VehicleForm
)
from db_manager.models import Vehicle
from django.views.generic.edit import CreateView

__all__ = ['VehicleCreateView']


class BaseVehicleCreateView(CreateView):
    model = Vehicle
    queryset = Vehicle.objects.all()
    template_name = 'crud/create.html'
    form_class = BaseVehicleForm
    _url = NotImplemented

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return redirect(self._url)


class VehicleCreateView(BaseVehicleCreateView):
    form_class = VehicleForm
    _url = 'index'

    def form_valid(self, form):
        form.instance._type = 0
        return super().form_valid(form)


class BrandCreateView(BaseVehicleCreateView):
    form_class = BrandForm
    _url = 'brand'

    def form_valid(self, form):
        form.instance._type = 0
        return super().form_valid(form)


class ModelCreateView(BaseVehicleCreateView):
    form_class = ModelForm
    _url = 'model'

    def form_valid(self, form):
        form.instance._type = 1
        return super().form_valid(form)


class GenerationCreateView(BaseVehicleCreateView):
    form_class = GenerationForm
    _url = 'generation'

    def form_valid(self, form):
        form.instance._type = 2
        return super().form_valid(form)


class RestylingCreateView(BaseVehicleCreateView):
    form_class = RestylingForm
    _url = 'restyling'

    def form_valid(self, form):
        form.instance._type = 3
        return super().form_valid(form)


class ConfigurationCreateView(BaseVehicleCreateView):
    form_class = ConfigurationForm
    _url = 'configuration'

    def form_valid(self, form):
        form.instance._type = 4
        return super().form_valid(form)
