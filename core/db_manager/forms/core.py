from typing import Optional, Union, Any

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


def get_model_choice_field_queryset(type_: int, cast_type: str = None) -> QuerySet:
    queryset = ParamsValue.objects.filter(type=type_)
    if cast_type:
        return queryset.extra(select={'casted_value': f'CAST(value AS {cast_type})'}).order_by('casted_value')
    return queryset.order_by('value')


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


wiper_length_common_queryset = get_model_choice_field_queryset(ParamsValue.Type.WIPERS_LENGTH, 'FLOAT')
WiperLength = make_class(
    'WiperLength',
    ['attributes', 'restrictions', 'wiper', 'length'],
    {
        'min': get_model_choice_field(wiper_length_common_queryset, 'Минимальная'),
        'max': get_model_choice_field(wiper_length_common_queryset, 'Максимальная'),
        'rec': get_model_choice_field(wiper_length_common_queryset, 'Рекомендуемая')
    },
    ['Дворник', 'Длина, мм'],
)

oil_queryset = get_model_choice_field_queryset(ParamsValue.Type.OIL_TYPE)
Oil = make_class(
    'Oil',
    ['attributes', 'restrictions', 'oil'],
    {
        'type': get_model_choice_field(oil_queryset, 'Рекомендуемый тип'),
        'viscosity': get_model_choice_field(oil_queryset, 'Рекомендуемая вязкость'),
    },
    'Масло'
)

rim_offset_queryset = get_model_choice_field_queryset(ParamsValue.Type.WHEEL_DEPARTURE, 'FLOAT')
RimOffset = make_class(
    'RimOffset',
    ['attributes', 'restrictions', 'rim', 'offset'],
    {
        'min': get_model_choice_field(rim_offset_queryset, 'Минимальный'),
        'max': get_model_choice_field(rim_offset_queryset, 'Максимальный'),
        'rec': get_model_choice_field(rim_offset_queryset, 'Рекомендуемый'),
    },
    ['Диски', 'Вынос'],
)

rim_center_hole_diameter_queryset = get_model_choice_field_queryset(ParamsValue.Type.WHEEL_CH_DIAMETER)
RimCenterHoleDiameter = make_class(
    'RimCenterHoleDiameter',
    ['attributes', 'restrictions', 'rim', 'center_hole_diameter'],
    {
        'rec': get_model_choice_field(rim_center_hole_diameter_queryset, 'Рекомендуемый'),
    },
    ['Диски', 'Диаметр ЦО'],
)

rim_diameter_queryset = get_model_choice_field_queryset(ParamsValue.Type.WHEEL_DIAMETER)
RimDiameter = make_class(
    'RimDiameter',
    ['attributes', 'restrictions', 'rim', 'diameter'],
    {
        'min': get_model_choice_field(rim_diameter_queryset, 'Минимальный'),
        'max': get_model_choice_field(rim_diameter_queryset, 'Максимальный'),
        'rec': get_model_choice_field(rim_diameter_queryset, 'Рекомендуемый')
    },
    ['Диски', 'Диаметр'],
)

rim_drilling_queryset = get_model_choice_field_queryset(ParamsValue.Type.WHEEL_DRILLING)
RimDrilling = make_class(
    'RimDrilling',
    ['attributes', 'restrictions', 'rim', 'drilling'],
    {
        'rec': get_model_choice_field(rim_drilling_queryset, 'Рекомендуемая')
    },
    ['Диски', 'Сверловка'],
)

rim_width_queryset = get_model_choice_field_queryset(ParamsValue.Type.WHEEL_WIDTH, 'FLOAT')
RimWidth = make_class(
    'RimWidth',
    ['attributes', 'restrictions', 'rim', 'width'],
    {
        'min': get_model_choice_field(rim_width_queryset, 'Минимальная'),
        'max': get_model_choice_field(rim_width_queryset, 'Максимальная'),
        'rec': get_model_choice_field(rim_width_queryset, 'Рекомендуемая')
    },
    ['Диски', 'Ширина'],
)

tire_diameter_queryset = get_model_choice_field_queryset(ParamsValue.Type.TIRE_DIAMETER, 'FLOAT')
TireDiameter = make_class(
    'TireDiameter',
    ['attributes', 'restrictions', 'tire', 'diameter'],
    {
        'min': get_model_choice_field(tire_diameter_queryset, 'Минимальный'),
        'max': get_model_choice_field(tire_diameter_queryset, 'Максимальный'),
        'rec': get_model_choice_field(tire_diameter_queryset, 'Рекомендуемый')
    },
    ['Шины', 'Диаметр'],
)

tire_height_queryset = get_model_choice_field_queryset(ParamsValue.Type.TIRE_INCH_HEIGHT, 'FLOAT')
TireHeight = make_class(
    'TireHeight',
    ['attributes', 'restrictions', 'tire', 'height'],
    {
        'min': get_model_choice_field(tire_height_queryset, 'Минимальная'),
        'max': get_model_choice_field(tire_height_queryset, 'Максимальная'),
        'rec': get_model_choice_field(tire_height_queryset, 'Рекомендуемая')
    },
    ['Шины', 'Высота профиля, %'],
)

tire_width_queryset = get_model_choice_field_queryset(ParamsValue.Type.TIRE_METRIC_WIDTH, 'FLOAT')
TireWidth = make_class(
    'TireWidth',
    ['attributes', 'restrictions', 'tire', 'width'],
    {
        'min': get_model_choice_field(tire_width_queryset, 'Минимальная'),
        'max': get_model_choice_field(tire_width_queryset, 'Максимальная'),
        'rec': get_model_choice_field(tire_width_queryset, 'Рекомендуемая')
    },
    ['Шины', 'Ширина'],
)
