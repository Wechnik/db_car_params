from django.shortcuts import redirect
from django.views.generic import UpdateView

from db_manager.models import ParamsValue
from db_manager.views.abstract import BaseLoginRequiredMixin
from db_manager.forms.params_value_form import BaseParamsForm, get_base_params_w_children_form


class BaseParamsValueUpdateView(BaseLoginRequiredMixin, UpdateView):
    model = ParamsValue
    queryset = ParamsValue.objects.all()
    template_name = 'crud/create.html'
    form_class = BaseParamsForm

    _url = NotImplemented
    _name = NotImplemented

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактировать {self._name}'
        return context

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return redirect(self._url)


class TireDiameterUpdateView(BaseParamsValueUpdateView):
    _url = 'tire_diameter'
    _name = 'диаметр шин'
    form_class = get_base_params_w_children_form('Доступная ширина', ParamsValue.Type.TIRE_INCH_WIDTH)


class TireMetricWidthUpdateView(BaseParamsValueUpdateView):
    _url = 'tire_metric_width'
    _name = 'ширину шины (метрическая)'


class TireMetricProfileUpdateView(BaseParamsValueUpdateView):
    _url = 'tire_metric_profile'
    _name = 'профиль шины (метрическая)'


class TireInchWidthUpdateView(BaseParamsValueUpdateView):
    _url = 'tire_inch_width'
    _name = 'ширина шины (дюймовая)'


class TireInchHeightUpdateView(BaseParamsValueUpdateView):
    _url = 'tire_inch_height'
    _name = 'высота шины (дюймовая)'


class WheelWidthUpdateView(BaseParamsValueUpdateView):
    _url = 'wheel_width'
    _name = 'ширина диска'


class WheelDiameterUpdateView(BaseParamsValueUpdateView):
    _url = 'wheel_diameter'
    _name = 'диаметр диска'
    form_class = get_base_params_w_children_form('Доступная ширина', ParamsValue.Type.WHEEL_WIDTH)


class WheelDrillingUpdateView(BaseParamsValueUpdateView):
    _url = 'wheel_drilling'
    _name = 'сверловка диска'
    form_class = get_base_params_w_children_form('Доступный диаметр', ParamsValue.Type.WHEEL_DIAMETER)


class WheelDepartureUpdateView(BaseParamsValueUpdateView):
    _url = 'wheel_departure'
    _name = 'вылет диска'


class WheelCHDiameterUpdateView(BaseParamsValueUpdateView):
    _url = 'wheel_ch_diameter'
    _name = 'диаметр центрального отверстия диска'


class OilTypeUpdateView(BaseParamsValueUpdateView):
    _url = 'oil_type'
    _name = 'тип масла'


class OilViscosityUpdateView(BaseParamsValueUpdateView):
    _url = 'oil_viscosity'
    _name = 'вязкость масла'


class WipersLengthUpdateView(BaseParamsValueUpdateView):
    _url = 'wipers_length'
    _name = 'длина дворников'


class YearUpdateView(BaseParamsValueUpdateView):
    _url = 'year'
    _name = 'год'


class BatteryCapacityUpdateView(BaseParamsValueUpdateView):
    _url = 'battery_capacity'
    _name = 'емкость аккумулятора'


class BatteryDimensionsUpdateView(BaseParamsValueUpdateView):
    _url = 'battery_dimensions'
    _name = 'габариты аккумулятора'


class BatteryStartingCurrentUpdateView(BaseParamsValueUpdateView):
    _url = 'battery_starting_current'
    _name = 'пусковой ток аккумулятора'


class BatteryPolarityUpdateView(BaseParamsValueUpdateView):
    _url = 'battery_polarity'
    _name = 'полярность аккумулятора'
