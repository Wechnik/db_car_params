from typing import Optional, List
from dataclasses import dataclass, is_dataclass

from django.db import models
from django.urls import reverse


class BaseRestriction:
    @classmethod
    def from_json(cls, attrs: dict):
        attrs = attrs or {}

        init_data = {}
        for cls_field_name, cls_field_type in cls.__annotations__.items():
            if is_dataclass(cls_field_type):
                init_data[cls_field_name] = cls_field_type.from_json(attrs.get(cls_field_name))
            else:
                init_data[cls_field_name] = attrs.get(cls_field_name)

        return cls(**init_data)

    def to_json(self) -> dict:
        json = {}
        for cls_field_name, cls_field_type in self.__annotations__.items():
            if is_dataclass(cls_field_type) and isinstance(getattr(self, cls_field_name), cls_field_type):
                json[cls_field_name] = getattr(self, cls_field_name).to_json()
            else:
                json[cls_field_name] = getattr(self, cls_field_name)
        return json


@dataclass
class Measurement(BaseRestriction):
    """Измерение."""

    min: int
    max: int
    rec: int


@dataclass
class Tire(BaseRestriction):
    """Покрышка."""

    width: Measurement
    height: Measurement
    diameter: Measurement


@dataclass
class Restriction(BaseRestriction):
    """Ограничение."""

    tire: Tire


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
        # Комплектация.
        CONFIGURATION = 3

    _type = models.IntegerField(choices=Type.choices)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    attrs = models.JSONField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs = self.attrs or {}
        self.restrictions = Restriction.from_json(self.attrs.get('restrictions'))

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.attrs['restrictions'] = self.restrictions.to_json()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

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
        return list(reversed(structure_data))
