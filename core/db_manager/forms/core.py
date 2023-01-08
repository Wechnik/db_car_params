from typing import Optional, Union, Any

from django.forms import IntegerField, ModelForm as ModelFormBase, CharField, TypedChoiceField

from db_manager.helpers import deepset
from db_manager.models import ParamsValue


def cleaned_data_to_json(cleaned_data: dict) -> dict:
    """Преобразовать заполненные данные формы в JSON-представление dataclass-атрибутов."""
    json = {}
    for field, value in cleaned_data.items():
        deepset(json, field, value)

    return json


def get_choices(choice_type) -> list[tuple[Any, Any]]:
    return [(None, '')] + [(choice.id, choice.value) for choice in ParamsValue.objects.filter(type=choice_type)]


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

wiper_length_common = {
    'choices': get_choices(ParamsValue.Type.WIPERS_LENGTH),
    'coerce': int,
}
WiperLength = make_class(
    'WiperLength',
    ['attributes', 'restrictions', 'wiper', 'length'],
    {
        'min': (TypedChoiceField, {
            **wiper_length_common,
            'label': 'Минимальная'
        }),
        'max': (TypedChoiceField, {
            **wiper_length_common,
            'label': 'Максимальная'
        }),
        'rec': (TypedChoiceField, {
            **wiper_length_common,
            'label': 'Рекомендуемая'
        })
    },
    ['Дворник', 'Длина, мм'],
)

Oil = make_class(
    'Oil',
    ['attributes', 'restrictions', 'oil'],
    {
        'type': (TypedChoiceField, {
            'choices': get_choices(ParamsValue.Type.OIL_TYPE),
            'coerce': int,
            'label': 'Рекомендуемый тип'
        }),
        'viscosity': (TypedChoiceField, {
            'choices': get_choices(ParamsValue.Type.OIL_VISCOSITY),
            'coerce': int,
            'label': 'Рекомендуемая вязкость'
        }),
    },
    'Масло'
)

rim_offset_common = {
    'choices': get_choices(ParamsValue.Type.WHEEL_DEPARTURE),
    'coerce': int,
}
RimOffset = make_class(
    'RimOffset',
    ['attributes', 'restrictions', 'rim', 'offset'],
    {
        'min': (TypedChoiceField, {
            **rim_offset_common,
            'label': 'Минимальный'
        }),
        'max': (TypedChoiceField, {
            **rim_offset_common,
            'label': 'Максимальный'
        }),
        'rec': (TypedChoiceField, {
            **rim_offset_common,
            'label': 'Рекомендуемый'
        })
    },
    ['Диски', 'Вынос'],
)

rim_center_hole_diameter_common = {
    'choices': get_choices(ParamsValue.Type.WHEEL_CH_DIAMETER),
    'coerce': int,
}
RimCenterHoleDiameter = make_class(
    'RimCenterHoleDiameter',
    ['attributes', 'restrictions', 'rim', 'center_hole_diameter'],
    {
        # 'min': (TypedChoiceField, {
        #     **rim_center_hole_diameter_common,
        #     'label': 'Минимальный'
        # }),
        # 'max': (TypedChoiceField, {
        #     **rim_center_hole_diameter_common,
        #     'label': 'Максимальный'
        # }),
        'rec': (TypedChoiceField, {
            **rim_center_hole_diameter_common,
            'label': 'Рекомендуемый'
        })
    },
    ['Диски', 'Диаметр ЦО'],
)

rim_diameter_common = {
    'choices': get_choices(ParamsValue.Type.WHEEL_DIAMETER),
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
        'rec': (TypedChoiceField, {
            'choices': get_choices(ParamsValue.Type.WHEEL_DRILLING),
            'coerce': int,
            'label': 'Рекомендуемая',
        })
    },
    ['Диски', 'Сверловка'],
)

rim_width_common = {
    'choices': get_choices(ParamsValue.Type.WHEEL_WIDTH),
    'coerce': int,
}
RimWidth = make_class(
    'RimWidth',
    ['attributes', 'restrictions', 'rim', 'width'],
    {
        'min': (TypedChoiceField, {
            **rim_width_common,
            'label': 'Минимальная',
        }),
        'max': (TypedChoiceField, {
            **rim_width_common,
            'label': 'Максимальная',
        }),
        'rec': (TypedChoiceField, {
            **rim_width_common,
            'label': 'Рекомендуемая',
        })
    },
    ['Диски', 'Ширина'],
)

tire_diameter_common = {
    'choices': get_choices(ParamsValue.Type.TIRE_DIAMETER),
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

tire_height_common = {
    'choices': get_choices(ParamsValue.Type.TIRE_INCH_HEIGHT),
    'coerce': int,
}
TireHeight = make_class(
    'TireHeight',
    ['attributes', 'restrictions', 'tire', 'height'],
    {
        'min': (TypedChoiceField, {
            **tire_height_common,
            'label': 'Минимальная',
        }),
        'max': (TypedChoiceField, {
            **tire_height_common,
            'label': 'Максимальная',
        }),
        'rec': (TypedChoiceField, {
            **tire_height_common,
            'label': 'Рекомендуемая',
        })
    },
    ['Шины', 'Высота профиля, %'],
)

tire_width_common = {
    'choices': get_choices(ParamsValue.Type.TIRE_METRIC_WIDTH),
    'coerce': int,
}
TireWidth = make_class(
    'TireWidth',
    ['attributes', 'restrictions', 'tire', 'width'],
    {
        'min': (TypedChoiceField, {
            **tire_width_common,
            'label': 'Минимальная',
        }),
        'max': (TypedChoiceField, {
            **tire_width_common,
            'label': 'Максимальная',
        }),
        'rec': (TypedChoiceField, {
            **tire_width_common,
            'label': 'Рекомендуемая',
        })
    },
    ['Шины', 'Ширина'],
)
