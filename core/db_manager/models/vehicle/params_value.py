from django.db import models
from django.urls import reverse


class ParamsValue(models.Model):
    """Модель таблицы для хранения значений параметров."""

    class Type(models.IntegerChoices):
        """Типы записей."""

        TIRE_DIAMETER = 0
        TIRE_METRIC_WIDTH = 1
        TIRE_METRIC_PROFILE = 2
        TIRE_INCH_WIDTH = 3
        TIRE_INCH_HEIGHT = 4
        WHEEL_WIDTH = 5
        WHEEL_DIAMETER = 6
        WHEEL_DRILLING = 7
        WHEEL_DEPARTURE = 8
        WHEEL_CH_DIAMETER = 9
        OIL_TYPE = 10
        OIL_VISCOSITY = 11
        WIPERS_LENGTH = 12

    type = models.IntegerField(choices=Type.choices)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value

    def get_absolute_url(self):
        return reverse('index')

    class Meta:
        db_table = 'db_manager_params_value'
