from django.template import Template, Context

from db_manager.forms.core import cleaned_data_to_json, WiperLength, Oil, RimOffset, \
    RimCenterHoleDiameter, RimDiameter, RimDrilling, RimWidth, TireDiameter, TireHeight, TireWidth
from db_manager.forms.crud_forms import BaseVehicleForm
from db_manager.models import Vehicle
from db_manager.models.vehicle.attributes import Attributes


class ConfigurationForm(BaseVehicleForm,
                        RimDiameter, RimDrilling, RimWidth, RimCenterHoleDiameter, RimOffset,
                        TireDiameter, TireWidth, TireHeight,
                        WiperLength,
                        Oil):
    class Meta:
        model = Vehicle
        fields = ['name', 'description']
        labels = {
            'name': 'Название',
            'description': 'Описание',
        }

    required = ('name',)

    template_name_div = 'configuration/div.html'

    def save(self, commit=True):
        self.instance.attributes = Attributes.from_json(cleaned_data_to_json(self.cleaned_data).get('attributes'))
        return super().save(commit=commit)

    def __init__(self, *args, **kwargs):
        BaseVehicleForm.__init__(self, *args, **kwargs)

        for base_type in type(self).mro():
            if hasattr(base_type, 'fill_initial'):
                base_type.fill_initial(self)

        def NestedDictValues(d):
            for v in d.values():
                if isinstance(v, dict):
                    yield from NestedDictValues(v)
                else:
                    yield v

        grouped_fields = []
        for field_group in NestedDictValues(self.field_groups):
            grouped_fields.extend(field_group)

        self.add_field_group('Параметры', [field for field in self.fields if field not in grouped_fields])

        for field in self.fields:
            if field not in self.required:
                self.fields[field].required = False
                self[field].required = False

    def form_content(self, form_content=None, level=2) -> list:
        target = self.field_groups if form_content is None else form_content

        levels = {
            0: 'h1',
            1: 'h2',
            2: 'h3',
            3: 'h4',
            4: 'h5',
            5: 'h6',
            6: 'p',
        }

        form_content = []
        for legend, content in target.items():
            if legend:
                tag = levels[level]
                form_content.append(Template(f'<{tag}>{legend}</{tag}>').render(Context({})))

            if isinstance(content, list):
                tags = []
                for field in content:
                    tags.append('<div class="col-4">')

                    if self[field].label:
                        tags.append(str(self[field].label_tag()))

                    if self[field].help_text:
                        tags.append(f'<div class="helptext">{{field.help_text | safe}}</div>')

                    tags.append(str(self[field]))
                    tags.append('</div>')

                wrapped_fields = tags
                form_content.append(
                    Template(f'<div class="row">{"".join([wrapped_field for wrapped_field in wrapped_fields])}</div>')
                    .render(Context({}))
                )
            else:
                form_content.extend(self.form_content(content, level + 1))

        return form_content
