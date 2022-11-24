from typing import Optional, List

from django.db import models
from django.urls import reverse


class Vehicle(models.Model):
    """Автомобиль/транспорт."""

    class Type(models.IntegerChoices):
        """Типы записей."""

        # Бренд/марка/производитель.
        BRAND = 0
        # Модель.
        MODEL = 1
        # Поколение.
        GENERATION = 2
        # Todo: Если рестайлинга в поколении не было (еще не было), то стоит добавить "пустой рест"?
        # Рестайлинг.
        RESTYLING = 3
        # Комплектация.
        CONFIGURATION = 4

    _type = models.IntegerField(choices=Type.choices)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    attrs = models.JSONField(null=True, blank=True)

    def __str__(self):
        display_name = self.name

        parent = self.parent
        while parent:
            display_name = f'{parent.name} {display_name}'

            parent = parent.parent

        return display_name

    def years_of_production(self) -> tuple[int, Optional[int]]:
        """Годы производства."""
        years_of_production = self.attrs.get('YearsOfProduction', {})
        return years_of_production.get('Start'), years_of_production.get('End')

    def get_absolute_url(self):
        return reverse('index')

    def get_structured_data(self) -> List[str]:
        """Возвращает информация об авто в структурированном виде."""
        structure_data = [self, self.name]
        parent = self.parent
        while parent:
            structure_data.append(parent.name)
            parent = parent.parent
        structure_data.reverse()
        return structure_data
