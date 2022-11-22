from django.forms.models import ModelForm

from db_manager.models import Vehicle


class VehicleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Vehicle
        fields = '__all__'
        labels = {
            '_type': 'Тип',
            'parent': 'Родитель',
            'name': 'Название',
            'description': 'Описание',
            'attrs': 'Дополнительные атрибуты',
        }
