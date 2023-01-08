from django.forms.models import ModelForm as ModelFormBase

from db_manager.helpers import deepset, deepget
from db_manager.models import Vehicle


class BaseVehicleForm(ModelFormBase):
    def __init__(self, *args, **kwargs):
        self.field_groups = {}
        ModelFormBase.__init__(self, *args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def add_field_group(self, path, fields):
        deepset(
            self.field_groups,
            path,
            deepget(self.field_groups, path, [] + fields)
        )

    class Meta:
        model = Vehicle
        fields = ['parent', 'name', 'description']
        labels = {
            'parent': 'Бренд',
            'name': 'Название',
            'description': 'Описание',
        }


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
