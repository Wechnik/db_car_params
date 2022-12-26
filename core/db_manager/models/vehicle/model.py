__all__ = ['Vehicle']

from typing import List

from django.db import models
from django.db.models import QuerySet
from django.urls import reverse

from db_manager.helpers import deepmerge
from db_manager.models.vehicle.attributes import Attributes


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
        self.attributes = Attributes.from_json(self.attrs)
        # Вроде jinja не падает, если атрибута нет
        self.selected = False

    @property
    def get_children(self) -> QuerySet:
        return Vehicle.objects.filter(parent=self)

    @property
    def get_hierarchy_attributes(self) -> Attributes:
        """Получить атрибуты. Поддержано наследование атрибутов."""
        obj = self
        attrs = {}
        while obj.parent:
            deepmerge(attrs, obj.attributes.to_json())
            obj = obj.parent

        return Attributes.from_json(attrs)

    # fixme: Костыль, связанный с serializer.
    @property
    def get_hierarchy_attributes_json(self) -> dict:
        """Получить атрибуты. Поддержано наследование атрибутов."""
        obj = self
        attrs = {}
        while obj.parent:
            deepmerge(attrs, obj.attributes.to_json())
            obj = obj.parent

        return attrs

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.attrs = self.attributes.to_json()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        display_name = self.name

        parent = self.parent
        while parent:
            display_name = f'{parent.name} {display_name}'

            parent = parent.parent

        return display_name

    # Fixme: Херня какая то
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
