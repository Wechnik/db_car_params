from django.shortcuts import render
from django.views.generic.base import View

from db_manager.models import ParamsValue
from db_manager.views.abstract import BaseLoginRequiredMixin


class BaseParamsView(BaseLoginRequiredMixin, View):
    """Базовый класс для отображения параметров."""

    title = NotImplemented
    type_param = NotImplemented
    type_view = NotImplemented

    def get(self, request, *args, **kwargs):
        """Метод отображения справочников параметров."""
        return render(
            request,
            'index.html',
            context={
                'title': self.title,
                'data': ParamsValue.objects.filter(type=self.type_param),
                'type': self.type_view,
            },
        )


class TireDiameterView(BaseParamsView):
    """Отображение параметра: Диаметр шин."""

    title = 'Диаметр шин'
    type_param = 0
    type_view = '_tire_diameter'


class TireMetricWidthView(BaseParamsView):
    """Отображение параметра: Ширина шины (метрическая)."""

    title = 'Ширина шины (метрическая)'
    type_param = 1
    type_view = '_tire_metric_width'


class TireMetricProfileView(BaseParamsView):
    """Отображение параметра: Профиль шины (метрическая)."""

    title = 'Профиль шины (метрическая)'
    type_param = 2
    type_view = '_tire_metric_profile'


class TireInchWidthView(BaseParamsView):
    """Отображение параметра: Ширина шины (дюймовая)."""

    title = 'Ширина шины (дюймовая)'
    type_param = 3
    type_view = '_tire_inch_width'


class TireInchHeightView(BaseParamsView):
    """Отображение параметра: Высота шины (дюймовая)."""

    title = 'Высота шины (дюймовая)'
    type_param = 4
    type_view = '_tire_inch_height'


class WheelWidthView(BaseParamsView):
    """Отображение параметра: Ширина диска."""

    title = 'Ширина диска'
    type_param = 5
    type_view = '_wheel_width'


class WheelDiameterView(BaseParamsView):
    """Отображение параметра: Диаметр диска."""

    title = 'Диаметр диска'
    type_param = 6
    type_view = '_wheel_diameter'


class WheelDrillingView(BaseParamsView):
    """Отображение параметра: Сверловка диска."""

    title = 'Сверловка диска'
    type_param = 7
    type_view = '_wheel_drilling'


class WheelDepartureView(BaseParamsView):
    """Отображение параметра: Вылет диска."""

    title = 'Вылет диска'
    type_param = 8
    type_view = '_wheel_departure'


class WheelCHDiameterView(BaseParamsView):
    """Отображение параметра: Диаметр центрального отверстия диска."""

    title = 'Диаметр центрального отверстия диска'
    type_param = 9
    type_view = '_wheel_ch_diameter'


class OilTypeView(BaseParamsView):
    """Отображение параметра: Тип масла."""

    title = 'Тип масла'
    type_param = 10
    type_view = '_oil_type'


class OilViscosityView(BaseParamsView):
    """Отображение параметра: Вязкость масла."""

    title = 'Вязкость масла'
    type_param = 11
    type_view = '_oil_viscosity'


class WipersLengthView(BaseParamsView):
    """Отображение параметра: Длина дворников."""

    title = 'Длина дворников'
    type_param = 12
    type_view = '_wipers_length'


class YearView(BaseParamsView):
    """Отображение параметра: Год."""

    title = 'Год'
    type_param = 13
    type_view = '_year'