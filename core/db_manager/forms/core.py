from django.db.models import QuerySet
from django.forms import ModelChoiceField
from django.forms.models import ModelChoiceIterator

from db_manager.helpers import deepset
from db_manager.models import ParamsValue


def cleaned_data_to_json(cleaned_data: dict) -> dict:
    """Преобразовать заполненные данные формы в JSON-представление dataclass-атрибутов."""
    json = {}
    for field, value in cleaned_data.items():
        deepset(json, field, value)

    return json


def get_model_choice_field_queryset(type_: int, sorter: callable = None) -> QuerySet:
    queryset = ParamsValue.objects.filter(type=type_)
    return sorter(queryset) if sorter else queryset.order_by('value')


class Iterator(ModelChoiceIterator):
    def choice(self, obj):
        return (
            obj.id,
            self.field.label_from_instance(obj),
        )


# Todo: Зачем это? Почему просто не используем ModelChoiceField?
class CustomField(ModelChoiceField):
    iterator = Iterator

    def to_python(self, value):
        return int(value) if value else None


def get_model_choice_field(queryset: QuerySet, label: str = None) -> CustomField:
    return CustomField(
        label=label,
        queryset=queryset,
        to_field_name='value',
    )


class Sorter:

    @staticmethod
    def sort_diameter(query_set: QuerySet) -> QuerySet:
        """"""
        return (query_set
                .extra(select={'float_value': 'regexp_replace(value, \'[^-0-9.]\', \'\', \'g\')::FLOAT'})
                .order_by('float_value'))

    @staticmethod
    def sort_drilling(query_set: QuerySet) -> QuerySet:
        """"""
        return (query_set
                .extra(select={'float_value': 'regexp_split_to_array(value, \'[^-0-9.]\')::FLOAT[]'})
                .order_by('float_value'))

    @staticmethod
    def sort_number(query_set: QuerySet) -> QuerySet:
        """"""
        try:
            return query_set.extra(select={'float_value': 'value::FLOAT'}).order_by('float_value')
        except Exception:
            return query_set.order_by('value')
