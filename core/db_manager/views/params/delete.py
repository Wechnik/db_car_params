from django.urls import reverse_lazy
from django.views.generic import DeleteView

from db_manager.models import ParamsValue
from db_manager.views.abstract import BaseLoginRequiredMixin


class BaseParamsValueDeleteView(BaseLoginRequiredMixin, DeleteView):
    model = ParamsValue
    template_name = 'params/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление параметра'
        return context


class TireDiameterDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('tire_diameter')


class TireMetricWidthDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('tire_metric_width')


class TireMetricProfileDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('tire_metric_profile')


class TireInchWidthDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('tire_inch_width')


class TireInchHeightDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('tire_inch_height')


class WheelWidthDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('wheel_width')


class WheelDiameterDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('wheel_diameter')


class WheelDrillingDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('wheel_drilling')


class WheelDepartureDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('wheel_departure')


class WheelCHDiameterDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('wheel_ch_diameter')


class OilTypeDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('oil_type')


class OilViscosityDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('oil_viscosity')


class WipersLengthDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('wipers_length')


class YearDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('year')


class BatteryCapacityDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('battery_capacity')


class BatteryDimensionsDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('battery_dimensions')


class BatteryStartingCurrentDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('battery_starting_current')


class BatteryPolarityDeleteView(BaseParamsValueDeleteView):
    success_url = reverse_lazy('battery_polarity')
