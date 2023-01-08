from typing import Optional, Union

from django.forms import IntegerField, ModelForm as ModelFormBase, CharField, TypedChoiceField

from db_manager.helpers import deepset


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


YearsOfProduction = make_class(
    'YearsOfProduction',
    ['attributes', 'years_of_production'],
    {
        'start': (TypedChoiceField, {
            'label': 'Начало',
            'choices': [(year, str(year)) for year in range(1950, 2024)],
            'coerce': int,
        }),
        'end': (TypedChoiceField, {
            'label': 'Конец',
            'choices': [(year, str(year)) for year in range(1950, 2024)],
            'coerce': int,
        })
    },
    'Годы выпуска',
)

WiperLength = make_class(
    'WiperLength',
    ['attributes', 'restrictions', 'wiper', 'length'],
    {
        'min': (IntegerField, {'label': 'Минимальная'}),
        'max': (IntegerField, {'label': 'Максимальная'}),
        'rec': (IntegerField, {'label': 'Рекомендуемая'})
    },
    ['Дворник', 'Длина'],
)

OilType = make_class(
    'OilType',
    ['attributes', 'restrictions', 'oil'],
    {
        'type': (CharField, {'label': 'Рекомендуемый тип'}),
    },
    'Масло'
)

RimOffset = make_class(
    'RimOffset',
    ['attributes', 'restrictions', 'rim', 'offset'],
    {
        'min': (IntegerField, {'label': 'Минимальный'}),
        'max': (IntegerField, {'label': 'Максимальный'}),
        'rec': (IntegerField, {'label': 'Рекомендуемый'})
    },
    ['Диски', 'Вынос'],
)

RimCenterHoleDiameter = make_class(
    'RimCenterHoleDiameter',
    ['attributes', 'restrictions', 'rim', 'center_hole_diameter'],
    {
        'min': (IntegerField, {'label': 'Минимальный'}),
        'max': (IntegerField, {'label': 'Максимальный'}),
        'rec': (IntegerField, {'label': 'Рекомендуемый'})
    },
    ['Диски', 'Диаметр ЦО'],
)

rim_diameter_common = {
    'choices': [(radius, f'R{radius}') for radius in range(1, 30)],
    'coerce': int,
}
RimDiameter = make_class(
    'RimDiameter',
    ['attributes', 'restrictions', 'rim', 'diameter'],
    {
        'min': (TypedChoiceField, {
            **rim_diameter_common,
            'label': 'Минимальный'
        }),
        'max': (TypedChoiceField, {
            **rim_diameter_common,
            'label': 'Максимальный'
        }),
        'rec': (TypedChoiceField, {
            **rim_diameter_common,
            'label': 'Рекомендуемый'
        })
    },
    ['Диски', 'Диаметр'],
)

RimDrilling = make_class(
    'RimDrilling',
    ['attributes', 'restrictions', 'rim', 'drilling'],
    {
        'min': (IntegerField, {'label': 'Минимальная'}),
        'max': (IntegerField, {'label': 'Максимальная'}),
        'rec': (IntegerField, {'label': 'Рекомендуемая'})
    },
    ['Диски', 'Сверловка'],
)

RimWidth = make_class(
    'RimWidth',
    ['attributes', 'restrictions', 'rim', 'width'],
    {
        'min': (IntegerField, {'label': 'Минимальная'}),
        'max': (IntegerField, {'label': 'Максимальная'}),
        'rec': (IntegerField, {'label': 'Рекомендуемая'})
    },
    ['Диски', 'Ширина'],
)

tire_diameter_common = {
    'choices': [(radius, f'R{radius}') for radius in range(1, 30)],
    'coerce': int,
}
TireDiameter = make_class(
    'TireDiameter',
    ['attributes', 'restrictions', 'tire', 'diameter'],
    {
        'min': (TypedChoiceField, {
            **tire_diameter_common,
            'label': 'Минимальный',
        }),
        'max': (TypedChoiceField, {
            **tire_diameter_common,
            'label': 'Максимальный',
        }),
        'rec': (TypedChoiceField, {
            **tire_diameter_common,
            'label': 'Рекомендуемый',
        })
    },
    ['Шины', 'Диаметр'],
)

TireHeight = make_class(
    'TireHeight',
    ['attributes', 'restrictions', 'tire', 'height'],
    {
        'min': (IntegerField, {'label': 'Минимальная'}),
        'max': (IntegerField, {'label': 'Максимальная'}),
        'rec': (IntegerField, {'label': 'Рекомендуемая'})
    },
    ['Шины', 'Высота профиля, %'],
)

TireWidth = make_class(
    'TireWidth',
    ['attributes', 'restrictions', 'tire', 'width'],
    {
        'min': (IntegerField, {'label': 'Минимальная'}),
        'max': (IntegerField, {'label': 'Максимальная'}),
        'rec': (IntegerField, {'label': 'Рекомендуемая'})
    },
    ['Шины', 'Ширина'],
)
