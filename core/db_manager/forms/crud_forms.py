from django.forms.models import ModelForm as ModelFormBase
from django.forms.fields import IntegerField

from db_manager.models import Vehicle, Attributes


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

    :param class_name: Название создаваемого класса.
    :param path:
    :param annotations:
    :return:
    """
    prefix = f'{("__".join(path + [""]))}'

    attrs = {
        f'{prefix}{cls_field_name}': cls_field_type(**cls_field_type_kwargs)
        for cls_field_name, (cls_field_type, cls_field_type_kwargs) in annotations.items()
    }

    def __init__(self: 'ModelFormBase', *args, **kwargs):
        ModelFormBase.__init__(self, *args, **kwargs)

    def fill_initial(self: 'ModelFormBase'):
        obj = self.instance
        for sub_object in path:
            obj = getattr(obj, sub_object)

        for cls_field_name in annotations:
            self.fields[f'{prefix}{cls_field_name}'].initial = getattr(obj, cls_field_name)

    return type(class_name, (ModelFormBase,), {
        '__init__': __init__,
        'fill_initial': fill_initial,
        **attrs,
    })


Width = make_class(
    'Width',
    ['attributes', 'restrictions', 'tire', 'width'],
    {
        'min': (IntegerField, {'label': 'Минимальная ширина'}),
        'max': (IntegerField, {'label': 'Максимальная ширина'}),
        'rec': (IntegerField, {'label': 'Рекомендуемая ширина'})
    }
)

Height = make_class(
    'Height',
    ['attributes', 'restrictions', 'tire', 'height'],
    {
        'min': (IntegerField, {'label': 'Минимальная высота профиля, %'}),
        'max': (IntegerField, {'label': 'Максимальная высота профиля, %'}),
        'rec': (IntegerField, {'label': 'Рекомендуемая высота профиля, %'})
    }
)

Diameter = make_class(
    'Diameter',
    ['attributes', 'restrictions', 'tire', 'diameter'],
    {
        'min': (IntegerField, {'label': 'Минимальный диаметр'}),
        'max': (IntegerField, {'label': 'Максимальный диаметр'}),
        'rec': (IntegerField, {'label': 'Рекомендуемый диаметр'})
    }
)

YearsOfProduction = make_class(
    'YearsOfProduction',
    ['attributes', 'years_of_production'],
    {
        'start': (IntegerField, {'label': 'Начало'}),
        'end': (IntegerField, {'label': 'Конец'})
    }
)


def deep_set(base_dict: dict, keys: str, value) -> None:
    _keys = keys.split('__')

    last_level = base_dict
    for i, key in enumerate(_keys[:-1]):
        if key not in last_level or not isinstance(last_level[key], dict):
            last_level[key] = {}
        last_level = last_level[key]
    last_level[_keys[-1]] = value


def cleaned_data_to_json(cleaned_data: dict) -> dict:
    json = {}
    for field, value in cleaned_data.items():
        deep_set(json, field, value)

    return json


class VehicleForm(BaseVehicleForm, Diameter, Width, Height, YearsOfProduction):
    template_name_div = 'div.html'

    def save(self, commit=True):
        self.instance.attributes = Attributes.from_json(cleaned_data_to_json(self.cleaned_data).get('attributes'))
        return super().save(commit=commit)

    def __init__(self, *args, **kwargs):
        Width.__init__(self, *args, **kwargs)
        Height.__init__(self, *args, **kwargs)
        Diameter.__init__(self, *args, **kwargs)
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
