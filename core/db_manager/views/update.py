from db_manager.forms.crud_forms import (
    BaseVehicleForm,
    BrandForm,
    ConfigurationForm,
    GenerationForm,
    ModelForm,
    RestylingForm
)
from db_manager.models import Vehicle
from django.views.generic.edit import UpdateView

__all__ = ['VehicleUpdateView']


class BaseVehicleUpdateView(UpdateView):
    model = Vehicle
    queryset = Vehicle.objects.all()
    template_name = 'crud/create.html'
    form_class = BaseVehicleForm


class VehicleUpdateView(BaseVehicleUpdateView):
    pass


class BrandUpdateView(BaseVehicleUpdateView):
    form_class = BrandForm

    def form_valid(self, form):
        form.instance._type = 0
        return super().form_valid(form)


class ModelUpdateView(BaseVehicleUpdateView):
    form_class = ModelForm

    def form_valid(self, form):
        form.instance._type = 1
        return super().form_valid(form)


class GenerationUpdateView(BaseVehicleUpdateView):
    form_class = GenerationForm

    def form_valid(self, form):
        form.instance._type = 2
        return super().form_valid(form)


class RestylingUpdateView(BaseVehicleUpdateView):
    form_class = RestylingForm

    def form_valid(self, form):
        form.instance._type = 3
        return super().form_valid(form)


class ConfigurationUpdateView(BaseVehicleUpdateView):
    form_class = ConfigurationForm

    def form_valid(self, form):
        form.instance._type = 4
        return super().form_valid(form)
