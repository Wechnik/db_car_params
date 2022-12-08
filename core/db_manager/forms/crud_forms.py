from django.forms.models import ModelForm as ModelFormBase
from django.forms.fields import IntegerField

from db_manager.helpers import deep_set
from db_manager.models import Vehicle
from db_manager.models.vehicle.attributes import Attributes


class BaseVehicleForm(ModelFormBase):
    def __init__(self, *args, **kwargs):
        ModelFormBase.__init__(self, *args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Vehicle
        fields = ['parent', 'name', 'description']
        labels = {
            'parent': 'Бренд',
            'name': 'Название',
            'description': 'Описание',
        }


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

    def __init__(self: 'ModelFormBase', *args, **kwargs):
        ModelFormBase.__init__(self, *args, **kwargs)

    def fill_initial(self: 'ModelFormBase') -> None:
        obj = self.instance
        for sub_object in self._path:
            obj = getattr(obj, sub_object)

        for cls_field_name in self._annotations:
            self.fields[f'{self._prefix}{cls_field_name}'].initial = getattr(obj, cls_field_name)

    return type(class_name, (ModelFormBase,), {
        '__init__': __init__,
        'fill_initial': fill_initial,
        '_path': path,
        '_annotations': annotations,
        '_prefix': prefix,
        **attrs,
    })


TireWidth = make_class(
    'TireWidth',
    ['attributes', 'restrictions', 'tire', 'width'],
    {
        'min': (IntegerField, {'label': 'Минимальная ширина шины'}),
        'max': (IntegerField, {'label': 'Максимальная ширина шины'}),
        'rec': (IntegerField, {'label': 'Рекомендуемая ширина шины'})
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

TireDiameter = make_class(
    'TireDiameter',
    ['attributes', 'restrictions', 'tire', 'diameter'],
    {
        'min': (IntegerField, {'label': 'Минимальный диаметр шины'}),
        'max': (IntegerField, {'label': 'Максимальный диаметр шины'}),
        'rec': (IntegerField, {'label': 'Рекомендуемый диаметр шины'})
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

RimHeight = make_class(
    'RimHeight',
    ['attributes', 'restrictions', 'rim', 'height'],
    {
        'min': (IntegerField, {'label': 'Минимальная высота диска'}),
        'max': (IntegerField, {'label': 'Максимальная высота диска'}),
        'rec': (IntegerField, {'label': 'Рекомендуемая высота диска'})
    }
)

RimDiameter = make_class(
    'RimDiameter',
    ['attributes', 'restrictions', 'rim', 'diameter'],
    {
        'min': (IntegerField, {'label': 'Минимальный диаметр диска'}),
        'max': (IntegerField, {'label': 'Максимальный диаметр диска'}),
        'rec': (IntegerField, {'label': 'Рекомендуемый диаметр диска'})
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

RimOffset = make_class(
    'RimOffset',
    ['attributes', 'restrictions', 'rim', 'offset'],
    {
        'min': (IntegerField, {'label': 'Минимальный вынос диска'}),
        'max': (IntegerField, {'label': 'Максимальный вынос диска'}),
        'rec': (IntegerField, {'label': 'Рекомендуемый вынос диска'})
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

YearsOfProduction = make_class(
    'YearsOfProduction',
    ['attributes', 'years_of_production'],
    {
        'start': (IntegerField, {'label': 'Год начала выпуска'}),
        'end': (IntegerField, {'label': 'Год окончания выпуска'})
    }
)


def cleaned_data_to_json(cleaned_data: dict) -> dict:
    """Преобразовать заполненные данные формы в JSON-представление dataclass-атрибутов."""
    json = {}
    for field, value in cleaned_data.items():
        deep_set(json, field, value)

    return json


class VehicleForm(BaseVehicleForm,
                  RimWidth, RimHeight, RimDiameter, RimCenterHoleDiameter, RimOffset,
                  TireDiameter, TireWidth, TireHeight,
                  WiperLength,
                  YearsOfProduction):
    template_name_div = 'div.html'

    def save(self, commit=True):
        self.instance = Vehicle.objects.get(id=self.request.POST.get('configurationId'))
        self.instance.attributes = Attributes.from_json(cleaned_data_to_json(self.cleaned_data).get('attributes'))
        return super().save(commit=commit)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        TireWidth.__init__(self, *args, **kwargs)
        TireHeight.__init__(self, *args, **kwargs)
        TireDiameter.__init__(self, *args, **kwargs)
        RimWidth.__init__(self, *args, **kwargs)
        RimHeight.__init__(self, *args, **kwargs)
        RimDiameter.__init__(self, *args, **kwargs)
        RimCenterHoleDiameter.__init__(self, *args, **kwargs)
        RimOffset.__init__(self, *args, **kwargs)
        WiperLength.__init__(self, *args, **kwargs)
        YearsOfProduction.__init__(self, *args, **kwargs)
        BaseVehicleForm.__init__(self, *args, **kwargs)

        for base_type in type(self).mro():
            if hasattr(base_type, 'fill_initial'):
                base_type.fill_initial(self)


class BrandForm(BaseVehicleForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'description']
        labels = {
            'name': 'Название',
            'description': 'Описание',
        }


class ModelForm(BaseVehicleForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Vehicle.objects.filter(_type=0)

    class Meta:
        model = Vehicle
        fields = ['parent', 'name', 'description']
        labels = {
            'parent': 'Бренд',
            'name': 'Название',
            'description': 'Описание',
        }


class GenerationForm(BaseVehicleForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Vehicle.objects.filter(_type=1)

    class Meta:
        model = Vehicle
        fields = ['parent', 'name', 'description']
        labels = {
            'parent': 'Модель',
            'name': 'Название',
            'description': 'Описание',
        }


class ConfigurationForm(BaseVehicleForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Vehicle.objects.filter(_type=2)

    class Meta:
        model = Vehicle
        fields = ['parent', 'name', 'description']
        labels = {
            'parent': 'Поколение',
            'name': 'Название',
            'description': 'Описание',
        }
