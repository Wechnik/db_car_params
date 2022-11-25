from django.forms.models import ModelForm
from django.forms.fields import IntegerField

from db_manager.models import Vehicle, Restriction, Tire, Measurement


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
    template_name_div = 'div.html'

    min_width = IntegerField(label='Минимальная ширина')
    max_width = IntegerField(label='Максимальная ширина')
    rec_width = IntegerField(label='Рекомендуемая ширина')

    min_height = IntegerField(label='Минимальная высота профиля %')
    max_height = IntegerField(label='Максимальная высота профиля %')
    rec_height = IntegerField(label='Рекомендуемая высота профиля %')

    min_diameter = IntegerField(label='Минимальный диаметр')
    max_diameter = IntegerField(label='Максимальный диаметр')
    rec_diameter = IntegerField(label='Рекомендуемый диаметр')

    def save(self, commit=True):
        self.instance.restrictions = Restriction(
            Tire(
                Measurement.from_json(self.cleaned_data),
                None,
                None,
            ),
        )
        return super().save(commit=commit)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_initial_fields()

    def _set_initial_fields(self):
        self.fields['min_width'].initial = self.instance.restrictions.tire.width.min
        self.fields['max_width'].initial = self.instance.restrictions.tire.width.max
        self.fields['rec_width'].initial = self.instance.restrictions.tire.width.rec

        self.fields['min_height'].initial = self.instance.restrictions.tire.height.min
        self.fields['max_height'].initial = self.instance.restrictions.tire.height.max
        self.fields['rec_height'].initial = self.instance.restrictions.tire.height.rec

        self.fields['min_diameter'].initial = self.instance.restrictions.tire.diameter.min
        self.fields['max_diameter'].initial = self.instance.restrictions.tire.diameter.max
        self.fields['rec_diameter'].initial = self.instance.restrictions.tire.diameter.rec


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
