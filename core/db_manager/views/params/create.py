from django.shortcuts import redirect
from django.views.generic import CreateView

from db_manager.forms.params_value_form import BaseParamsForm, get_base_params_w_children_form
from db_manager.models import ParamsValue
from db_manager.views.abstract import BaseLoginRequiredMixin


class BaseParamsValueCreateView(BaseLoginRequiredMixin, CreateView):
    model = ParamsValue
    queryset = ParamsValue.objects.all()
    template_name = 'crud/create.html'
    form_class = BaseParamsForm

    _url = NotImplemented
    _name = NotImplemented

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Создать {self._name}'
        return context

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return redirect(self._url)


class TireDiameterCreateView(BaseParamsValueCreateView):

    _url = 'tire_diameter'
    _name = 'диаметр шин'
    form_class = get_base_params_w_children_form('Доступная ширина', ParamsValue.Type.TIRE_INCH_WIDTH)

    def form_valid(self, form):
        form.instance.type = 0
        return super().form_valid(form)


class TireMetricWidthCreateView(BaseParamsValueCreateView):

    _url = 'tire_metric_width'
    _name = 'ширину шины (метрическая)'

    def form_valid(self, form):
        form.instance.type = 1
        return super().form_valid(form)


class TireMetricProfileCreateView(BaseParamsValueCreateView):

    _url = 'tire_metric_profile'
    _name = 'профиль шины (метрическая)'

    def form_valid(self, form):
        form.instance.type = 2
        return super().form_valid(form)


class TireInchWidthCreateView(BaseParamsValueCreateView):

    _url = 'tire_inch_width'
    _name = 'ширина шины (дюймовая)'

    def form_valid(self, form):
        form.instance.type = 3
        return super().form_valid(form)


class TireInchHeightCreateView(BaseParamsValueCreateView):

    _url = 'tire_inch_height'
    _name = 'высота шины (дюймовая)'

    def form_valid(self, form):
        form.instance.type = 4
        return super().form_valid(form)


class WheelWidthCreateView(BaseParamsValueCreateView):

    _url = 'wheel_width'
    _name = 'ширина диска'

    def form_valid(self, form):
        form.instance.type = 5
        return super().form_valid(form)


class WheelDiameterCreateView(BaseParamsValueCreateView):

    _url = 'wheel_diameter'
    _name = 'диаметр диска'
    form_class = get_base_params_w_children_form('Доступная ширина', ParamsValue.Type.WHEEL_WIDTH)

    def form_valid(self, form):
        form.instance.type = 6
        return super().form_valid(form)


class WheelDrillingCreateView(BaseParamsValueCreateView):

    _url = 'wheel_drilling'
    _name = 'сверловка диска'
    form_class = get_base_params_w_children_form('Доступный диаметр', ParamsValue.Type.WHEEL_DIAMETER)

    def form_valid(self, form):
        form.instance.type = 7
        return super().form_valid(form)


class WheelDepartureCreateView(BaseParamsValueCreateView):

    _url = 'wheel_departure'
    _name = 'вылет диска'

    def form_valid(self, form):
        form.instance.type = 8
        return super().form_valid(form)


class WheelCHDiameterCreateView(BaseParamsValueCreateView):

    _url = 'wheel_ch_diameter'
    _name = 'диаметр центрального отверстия диска'

    def form_valid(self, form):
        form.instance.type = 9
        return super().form_valid(form)


class OilTypeCreateView(BaseParamsValueCreateView):

    _url = 'oil_type'
    _name = 'тип масла'

    def form_valid(self, form):
        form.instance.type = 10
        return super().form_valid(form)


class OilViscosityCreateView(BaseParamsValueCreateView):

    _url = 'oil_viscosity'
    _name = 'вязкость масла'

    def form_valid(self, form):
        form.instance.type = 11
        return super().form_valid(form)


class WipersLengthCreateView(BaseParamsValueCreateView):
    _url = 'wipers_length'
    _name = 'длина дворников'

    def form_valid(self, form):
        form.instance.type = 12
        return super().form_valid(form)


class YearCreateView(BaseParamsValueCreateView):
    _url = 'year'
    _name = 'год'

    def form_valid(self, form):
        form.instance.type = 13
        return super().form_valid(form)


class BatteryCapacityCreateView(BaseParamsValueCreateView):
    _url = 'battery_capacity'
    _name = 'емкость аккумулятора'

    def form_valid(self, form):
        form.instance.type = 14
        return super().form_valid(form)


class BatteryDimensionsCreateView(BaseParamsValueCreateView):
    _url = 'battery_dimensions'
    _name = 'габариты аккумулятора'

    def form_valid(self, form):
        form.instance.type = 15
        return super().form_valid(form)


class BatteryStartingCurrentCreateView(BaseParamsValueCreateView):
    _url = 'battery_starting_current'
    _name = 'пусковой ток аккумулятора'

    def form_valid(self, form):
        form.instance.type = 16
        return super().form_valid(form)


class BatteryPolarityCreateView(BaseParamsValueCreateView):
    _url = 'battery_polarity'
    _name = 'полярность аккумулятора'

    def form_valid(self, form):
        form.instance.type = 17
        return super().form_valid(form)
