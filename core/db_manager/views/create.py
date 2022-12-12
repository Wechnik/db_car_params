from db_manager.forms.crud_forms import BaseVehicleForm, BrandForm, GenerationForm, ModelForm
from db_manager.models import Vehicle
from db_manager.views.abstract import BaseLoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.edit import CreateView


class BaseVehicleCreateView(BaseLoginRequiredMixin, CreateView):
    model = Vehicle
    queryset = Vehicle.objects.all()
    template_name = 'crud/create.html'
    form_class = BaseVehicleForm

    _url = NotImplemented
    _name = NotImplemented

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Создать {self._name}'
        return context

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return redirect(self._url)


class BrandCreateView(BaseVehicleCreateView):
    form_class = BrandForm
    _url = 'brand'
    _name = 'бренд'

    def form_valid(self, form):
        form.instance._type = 0
        return super().form_valid(form)


class ModelCreateView(BaseVehicleCreateView):
    form_class = ModelForm
    _url = 'model'
    _name = 'модель'

    def form_valid(self, form):
        form.instance._type = 1
        return super().form_valid(form)


class GenerationCreateView(BaseVehicleCreateView):
    form_class = GenerationForm
    _url = 'generation'
    _name = 'поколение'

    def form_valid(self, form):
        form.instance._type = 2
        return super().form_valid(form)
