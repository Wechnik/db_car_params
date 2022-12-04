import re
from typing import List
from dataclasses import dataclass, is_dataclass

from django.db import models
from django.urls import reverse

from db_manager.helpers import deepmerge


class CaseHelper:
    """Вспомогательный класс для работы с регистрами."""

    @staticmethod
    def snake_to_camel(text: str) -> str:
        """Преобразовать строку из snake_case в camelCase."""
        words = text.split('_')
        if len(words) > 1:
            first, *rest = words
            words = [first] + list(map(lambda word: word.capitalize(), rest))
        return ''.join(words)

    @staticmethod
    def camel_to_snake(text: str) -> str:
        """Преобразовать строку из camelCase в snake_case."""
        return '_'.join(map(lambda txt: txt.lower(), re.findall(r'((?:[A-Z]+|\A)[a-z]*)', text)))


class BaseAttribute:
    """Базовый аттрибут. Вспомогательный класс для работы с dataclass."""

    @classmethod
    def from_json(cls, json_repr: dict):
        """
        Сформировать dataclass из JSON. Поддерживает неограниченную вложенность dataclass.
        :param json_repr: JSON-представление dataclass.
        :return: dataclass, заполненный из JSON.
        """
        json_repr = json_repr or {}

        init_data = {}
        for cls_field_name, cls_field_type in cls.__annotations__.items():
            if is_dataclass(cls_field_type):
                init_data[cls_field_name] = cls_field_type.from_json(json_repr.get(cls_field_name))
            else:
                init_data[cls_field_name] = json_repr.get(cls_field_name)

        return cls(**init_data)

    def to_json(self) -> dict:
        """Получить JSON-представление dataclass. Поддерживает неограниченный уровень вложенности dataclass."""
        json = {}
        for cls_field_name, cls_field_type in self.__annotations__.items():
            if is_dataclass(cls_field_type) and isinstance(getattr(self, cls_field_name), cls_field_type):
                json[cls_field_name] = getattr(self, cls_field_name).to_json()
            else:
                json[cls_field_name] = getattr(self, cls_field_name)

        return json


@dataclass
class Measurement(BaseAttribute):
    """Измерение."""

    min: int
    max: int
    rec: int


@dataclass
class Tire(BaseAttribute):
    """Покрышка."""

    width: Measurement
    height: Measurement
    diameter: Measurement


@dataclass
class Restrictions(BaseAttribute):
    """Ограничение."""

    tire: Tire


@dataclass
class YearsOfProduction(BaseAttribute):
    """Годы производства."""

    start: int
    end: int

    def __str__(self):
        if not self.start:
            return ''
        if self.end:
            return f'{self.start} - {self.end}'
        else:
            return f'С {self.start}'


@dataclass
class Attributes(BaseAttribute):
    """Атрибуты."""

    years_of_production: YearsOfProduction
    restrictions: Restrictions


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

    @property
    def get_hierarchy_attributes(self) -> Attributes:
        """Получить атрибуты. Поддержано наследование атрибутов."""
        obj = self
        attrs = {}
        while obj.parent:
            deepmerge(attrs, obj.attributes.to_json())
            obj = obj.parent

        return Attributes.from_json(attrs)

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
