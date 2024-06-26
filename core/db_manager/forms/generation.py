from db_manager.forms.core import cleaned_data_to_json
from db_manager.forms.crud_forms import BaseVehicleForm
from db_manager.models import Vehicle
from db_manager.models.vehicle.attributes import Attributes


class GenerationForm(BaseVehicleForm):
    class Meta:
        model = Vehicle
        fields = ['parent', 'name', 'description']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'parent': 'Модель',
        }

    template_name_div = 'div.html'

    def save(self, commit=True):
        self.instance.attributes = Attributes.from_json(cleaned_data_to_json(self.cleaned_data).get('attributes'))
        return super().save(commit=commit)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Vehicle.objects.filter(_type=Vehicle.Type.MODEL.value)
