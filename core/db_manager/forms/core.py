from django.forms import IntegerField, ModelForm as ModelFormBase, CharField, TypedChoiceField

from db_manager.helpers import deep_set


def cleaned_data_to_json(cleaned_data: dict) -> dict:
    """Преобразовать заполненные данные формы в JSON-представление dataclass-атрибутов."""
    json = {}
    for field, value in cleaned_data.items():
        deep_set(json, field, value)

    return json


def make_class(class_name: str, path: list[str], annotations: dict):
    """
    Сформировать класс для работы с атрибутами как полями формы.
    :param class_name: Название создаваемого класса.
    :param path: Путь до атрибута (dataclass).
    :param annotations: Аннотации. Содержат название конечного атрибута не (dataclass).
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
        obj = self.instance
        for sub_object in path:
            obj = getattr(obj, sub_object)

        for cls_field_name in annotations:
            self.fields[f'{prefix}{cls_field_name}'].initial = getattr(obj, cls_field_name)

    return type(class_name, (ModelFormBase,), {
        'fill_initial': fill_initial,
        **attrs,
    })


YearsOfProduction = make_class(
    'YearsOfProduction',
    ['attributes', 'years_of_production'],
    {
        'start': (TypedChoiceField, {
            'label': 'Год начала выпуска',
            'choices': [(year, str(year)) for year in range(1950, 2024)],
            'coerce': int,
        }),
        'end': (TypedChoiceField, {
            'label': 'Год окончания выпуска',
            'choices': [(year, str(year)) for year in range(1950, 2024)],
            'coerce': int,
        })
    }
)

WiperLength = make_class(
    'WiperLength',
    ['attributes', 'restrictions', 'wiper', 'length'],
    {
        'min': (IntegerField, {'label': 'Минимальная длина дворника'}),
        'max': (IntegerField, {'label': 'Максимальная длина дворника'}),
        'rec': (IntegerField, {'label': 'Рекомендуемая длина дворника'})
    }
)

OilType = make_class(
    'OilType',
    ['attributes', 'restrictions', 'oil'],
    {
        'type': (CharField, {'label': 'Рекомендуемый тип масла'}),
    }
)

RimOffset = make_class(
    'RimOffset',
    ['attributes', 'restrictions', 'rim', 'offset'],
    {
        'min': (IntegerField, {'label': 'Минимальный вынос диска'}),
        'max': (IntegerField, {'label': 'Максимальный вынос диска'}),
        'rec': (IntegerField, {'label': 'Рекомендуемый вынос диска'})
    }
)

RimCenterHoleDiameter = make_class(
    'RimCenterHoleDiameter',
    ['attributes', 'restrictions', 'rim', 'center_hole_diameter'],
    {
        'min': (IntegerField, {'label': 'Минимальный диаметр ЦО диска'}),
        'max': (IntegerField, {'label': 'Максимальный диаметр ЦО диска'}),
        'rec': (IntegerField, {'label': 'Рекомендуемый диаметр ЦО диска'})
    }
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
            'label': 'Минимальный диаметр диска'
        }),
        'max': (TypedChoiceField, {
            **rim_diameter_common,
            'label': 'Максимальный диаметр диска'
        }),
        'rec': (TypedChoiceField, {
            **rim_diameter_common,
            'label': 'Рекомендуемый диаметр диска'
        })
    }
)

RimDrilling = make_class(
    'RimDrilling',
    ['attributes', 'restrictions', 'rim', 'drilling'],
    {
        'min': (IntegerField, {'label': 'Минимальная XXX диска'}),
        'max': (IntegerField, {'label': 'Максимальная XXX диска'}),
        'rec': (IntegerField, {'label': 'Рекомендуемая XXX диска'})
    }
)

RimWidth = make_class(
    'RimWidth',
    ['attributes', 'restrictions', 'rim', 'width'],
    {
        'min': (IntegerField, {'label': 'Минимальная ширина диска'}),
        'max': (IntegerField, {'label': 'Максимальная ширина диска'}),
        'rec': (IntegerField, {'label': 'Рекомендуемая ширина диска'})
    }
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
            'label': 'Минимальный диаметр шины',
        }),
        'max': (TypedChoiceField, {
            **tire_diameter_common,
            'label': 'Максимальный диаметр шины',
        }),
        'rec': (TypedChoiceField, {
            **tire_diameter_common,
            'label': 'Рекомендуемый диаметр шины',
        })
    }
)

TireHeight = make_class(
    'TireHeight',
    ['attributes', 'restrictions', 'tire', 'height'],
    {
        'min': (IntegerField, {'label': 'Минимальная высота профиля шины, %'}),
        'max': (IntegerField, {'label': 'Максимальная высота профиля шины, %'}),
        'rec': (IntegerField, {'label': 'Рекомендуемая высота профиля шины, %'})
    }
)

TireWidth = make_class(
    'TireWidth',
    ['attributes', 'restrictions', 'tire', 'width'],
    {
        'min': (IntegerField, {'label': 'Минимальная ширина шины'}),
        'max': (IntegerField, {'label': 'Максимальная ширина шины'}),
        'rec': (IntegerField, {'label': 'Рекомендуемая ширина шины'})
    }
)
