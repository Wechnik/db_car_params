from typing import Optional, Union

from django.db.models import QuerySet
from django.forms import IntegerField, ModelForm as ModelFormBase, ModelChoiceField
from django.forms.models import ModelChoiceIterator

from db_manager.helpers import deepset
from db_manager.models import ParamsValue


def cleaned_data_to_json(cleaned_data: dict) -> dict:
    """Преобразовать заполненные данные формы в JSON-представление dataclass-атрибутов."""
    json = {}
    for field, value in cleaned_data.items():
        deepset(json, field, value)

    return json


def make_class(class_name: str, path: list[str], annotations: dict[str, tuple[type, dict[str]]],
               group: Optional[Union[str, list[str]]] = None) -> type:
    """
    Сформировать класс для работы с атрибутами как полями формы.
    :param class_name: Название создаваемого класса.
    :param path: Путь до атрибута (dataclass).
    :param annotations: Аннотации. Содержат название конечного атрибута не (dataclass).
    :param group: .
    :return: Класс содержит:
        - Атрибуты класса в виде названия полей с сохранением иерархии.
        - Instance-метод fill_initial для заполнения полей.
        - __init__-метод от ModelFormBase.

        Пример:
        >>> make_class(
        >>>     class_name='Width',
        >>>     path=['attributes', 'restrictions', 'tire', 'width'],
        >>>     annotations={
        >>>        'min': (IntegerField, {'label': 'Минимальная ширина'}),
        >>>        'max': (IntegerField, {'label': 'Максимальная ширина'}),
        >>>     }
        >>> )

        Эквивалентно:
        >>> Width(ModelFormBase):
        >>>    attributes__restrictions__tire__width__min: IntegerField
        >>>    attributes__restrictions__tire__width__max: IntegerField
        >>>
        >>>    def fill_initial(self) -> None:
        >>>        ...
    """
    prefix = f'{("__".join(path + [""]))}'

    attrs = {
        f'{prefix}{cls_field_name}': cls_field_type(**cls_field_type_kwargs)
        for cls_field_name, (cls_field_type, cls_field_type_kwargs) in annotations.items()
    }

    def fill_initial(self: 'ModelFormBase') -> None:
        """Заполнить форму данными из модели."""
        if getattr(self, 'initial_attributes', None):
            class obj:
                attributes = self.initial_attributes
        else:
            obj = self.instance

        for sub_object in path:
            obj = getattr(obj, sub_object)

        # Заполняем поля первичными данными.
        fields = []
        for cls_field_name in annotations:
            self.fields[f'{prefix}{cls_field_name}'].initial = getattr(obj, cls_field_name)
            fields.append(f'{prefix}{cls_field_name}')

        self.add_field_group(group or '', fields)

    return type(class_name, (ModelFormBase,), {
        'fill_initial': fill_initial,
        **attrs,
    })


def get_model_choice_field_queryset(type_: int, sorter: callable = None) -> QuerySet:
    queryset = ParamsValue.objects.filter(type=type_)
    return sorter(queryset) if sorter else queryset.order_by('value')


class Iterator(ModelChoiceIterator):
    def choice(self, obj):
        return (
            obj.id,
            self.field.label_from_instance(obj),
        )


class CustomField(ModelChoiceField):
    iterator = Iterator

    def to_python(self, value):
        return int(value) if value else None


def get_model_choice_field(queryset: QuerySet, label: str = None) -> tuple[type, dict]:
    return (CustomField, {
        'label': label,
        'queryset': queryset,
        'to_field_name': 'value',
    })


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


wiper_length_common_queryset = get_model_choice_field_queryset(ParamsValue.Type.WIPERS_LENGTH, Sorter.sort_number)
WiperLength = make_class(
    'WiperLength',
    ['attributes', 'restrictions', 'wiper', 'length'],
    {
        'rec': get_model_choice_field(wiper_length_common_queryset, 'Длина, мм')
    },
    ['Дворник'],
)

Oil = make_class(
    'Oil',
    ['attributes', 'restrictions', 'oil'],
    {
        'type': get_model_choice_field(
            get_model_choice_field_queryset(ParamsValue.Type.OIL_TYPE),
            'Тип'
        ),
        'viscosity': get_model_choice_field(
            get_model_choice_field_queryset(ParamsValue.Type.OIL_VISCOSITY),
            'Вязкость'
        ),
    },
    'Масло'
)

rim_offset_queryset = get_model_choice_field_queryset(ParamsValue.Type.WHEEL_DEPARTURE, Sorter.sort_number)
RimOffset = make_class(
    'RimOffset',
    ['attributes', 'restrictions', 'rim', 'offset'],
    {
        'rec': get_model_choice_field(rim_offset_queryset, 'Вынос'),
    },
    ['Диски'],
)

rim_center_hole_diameter_queryset = get_model_choice_field_queryset(ParamsValue.Type.WHEEL_CH_DIAMETER,
                                                                    Sorter.sort_number)
RimCenterHoleDiameter = make_class(
    'RimCenterHoleDiameter',
    ['attributes', 'restrictions', 'rim', 'center_hole_diameter'],
    {
        'rec': get_model_choice_field(rim_center_hole_diameter_queryset, 'Диаметр ЦО'),
    },
    ['Диски'],
)

rim_diameter_queryset = get_model_choice_field_queryset(ParamsValue.Type.WHEEL_DIAMETER, Sorter.sort_diameter)
RimDiameter = make_class(
    'RimDiameter',
    ['attributes', 'restrictions', 'rim', 'diameter'],
    {
        'rec': get_model_choice_field(rim_diameter_queryset, 'Диаметр')
    },
    'Диски',
)

rim_drilling_queryset = get_model_choice_field_queryset(ParamsValue.Type.WHEEL_DRILLING, Sorter.sort_drilling)
RimDrilling = make_class(
    'RimDrilling',
    ['attributes', 'restrictions', 'rim', 'drilling'],
    {
        'rec': get_model_choice_field(rim_drilling_queryset, 'Сверловка')
    },
    'Диски',
)

rim_width_queryset = get_model_choice_field_queryset(ParamsValue.Type.WHEEL_WIDTH, Sorter.sort_number)
RimWidth = make_class(
    'RimWidth',
    ['attributes', 'restrictions', 'rim', 'width'],
    {
        'rec': get_model_choice_field(rim_width_queryset, 'Ширина')
    },
    'Диски',
)

tire_diameter_queryset = get_model_choice_field_queryset(ParamsValue.Type.TIRE_DIAMETER, Sorter.sort_number)
TireDiameter = make_class(
    'TireDiameter',
    ['attributes', 'restrictions', 'tire', 'diameter'],
    {
        'rec': get_model_choice_field(tire_diameter_queryset, 'Диаметр')
    },
    'Шины',
)

tire_height_queryset = get_model_choice_field_queryset(ParamsValue.Type.TIRE_INCH_HEIGHT, Sorter.sort_number)
TireHeight = make_class(
    'TireHeight',
    ['attributes', 'restrictions', 'tire', 'height'],
    {
        'rec': get_model_choice_field(tire_height_queryset, 'Высота профиля, %')
    },
    'Шины',
)

tire_width_queryset = get_model_choice_field_queryset(ParamsValue.Type.TIRE_METRIC_WIDTH, Sorter.sort_number)
TireWidth = make_class(
    'TireWidth',
    ['attributes', 'restrictions', 'tire', 'width'],
    {
        'rec': get_model_choice_field(tire_width_queryset, 'Ширина')
    },
    'Шины',
)
