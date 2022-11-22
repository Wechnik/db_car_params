from django.forms.models import ModelForm

from db_manager.models import Vehicle


class BaseVehicleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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


class VehicleForm(BaseVehicleForm):
    pass


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


class RestylingForm(BaseVehicleForm):

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


class ConfigurationForm(BaseVehicleForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Vehicle.objects.filter(_type=3)

    class Meta:
        model = Vehicle
        fields = ['parent', 'name', 'description']
        labels = {
            'parent': 'Рестайлинг',
            'name': 'Название',
            'description': 'Описание',
        }
