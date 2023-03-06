from django.forms import CheckboxSelectMultiple
from django.forms.models import ModelForm, ModelMultipleChoiceField

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


def get_base_params_w_children_form(label: str, child_param_type: ParamsValue.Type):
    class BaseParamsWChildrenForm(BaseParamsForm):
        children = ModelMultipleChoiceField(
            label=label,
            queryset=ParamsValue.objects.filter(type=child_param_type).order_by('value'),
            to_field_name='id',
            # widget=CheckboxSelectMultiple(),
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['children'].initial = ParamsValue.objects.filter(type=child_param_type, parent=self.instance.id)

        def save(self, commit=True):
            ParamsValue.objects.filter(type=child_param_type, parent=self.instance.id).update(parent=None)
            self.cleaned_data.get('children').update(parent=self.instance.id)
            return super().save(commit=commit)

    return BaseParamsWChildrenForm
