from django.forms.models import ModelForm

from db_manager.models import ParamsValue


class BaseParamsForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ParamsValue
        fields = ['value']
        labels = {
            'value': 'Значение',
        }
