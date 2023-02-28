from typing import Union

from django.forms import ModelChoiceField, Select
from django.forms.models import ModelChoiceIterator
from django.template import Template, Context
from django.utils.safestring import SafeString

from db_manager.forms.core import cleaned_data_to_json, WiperLength, Oil, RimOffset, \
    RimCenterHoleDiameter, RimDiameter, RimDrilling, RimWidth, TireDiameter, TireHeight, TireWidth
from db_manager.forms.crud_forms import BaseVehicleForm
from db_manager.models import Vehicle, ParamsValue
from db_manager.models.vehicle.attributes import Attributes


class Iterator(ModelChoiceIterator):
    def choice(self, obj):
        return obj.id, obj.name


class CustomField(ModelChoiceField):
    iterator = Iterator


class CustomSelect(Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['data-parent'] = value.instance.parent.id
        return option


def get_id_from_obj(obj):
    return obj.id if obj is not None else None


class ConfigurationForm(BaseVehicleForm,
                        RimDiameter, RimDrilling, RimWidth, RimCenterHoleDiameter, RimOffset,
                        TireDiameter, TireWidth, TireHeight,
                        WiperLength,
                        Oil):
    brand = CustomField(
        label='Брэнд',
        queryset=Vehicle.objects.filter(_type=Vehicle.Type.BRAND.value),
        to_field_name='id',
        required=True,
        widget=Select(attrs={'onChange': 'onSelectChange(this);', 'data-child': 'model'}),
    )
    model = ModelChoiceField(
        label='Модель',
        queryset=Vehicle.objects.filter(_type=Vehicle.Type.MODEL.value),
        to_field_name='id',
        required=True,
        widget=CustomSelect(attrs={'onChange': 'onSelectChange(this);', 'data-child': 'generation'})
    )
    generation = ModelChoiceField(
        label='Поколение',
        queryset=Vehicle.objects.filter(_type=Vehicle.Type.GENERATION.value),
        to_field_name='id',
        required=True,
        widget=CustomSelect(),
    )
    start_year = ModelChoiceField(
        label='Начало',
        queryset=ParamsValue.objects.filter(type=ParamsValue.Type.YEAR).order_by('value'),
        to_field_name='id',
    )
    end_year = ModelChoiceField(
        label='Конец',
        queryset=ParamsValue.objects.filter(type=ParamsValue.Type.YEAR).order_by('value'),
        to_field_name='id'
    )

    parental_fields = ['brand', 'model', 'generation', 'start_year', 'end_year']

    class Meta:
        model = Vehicle
        fields = ['name', 'description']
        labels = {
            'name': 'Название',
            'description': 'Описание',
        }

    required = ('name', 'brand', 'model', 'generation')

    template_name_div = 'configuration/div.html'

    def save(self, commit=True):
        self.instance.attributes = Attributes.from_json(cleaned_data_to_json(self.cleaned_data).get('attributes'))

        self.instance.parent = self.cleaned_data.get('generation')
        self.instance.parent.parent = self.cleaned_data.get('model')
        self.instance.parent.attributes.years_of_production.start = get_id_from_obj(self.cleaned_data.get('start_year'))
        self.instance.parent.attributes.years_of_production.end = get_id_from_obj(self.cleaned_data.get('end_year'))
        self.instance.parent.save()

        return super().save(commit=commit)

    def __init__(self, *args, **kwargs):
        self.initial_attributes = kwargs.pop('initial_attributes') if 'initial_attributes' in kwargs else None
        parent = kwargs.pop('parent') if 'parent' in kwargs else None

        BaseVehicleForm.__init__(self, *args, **kwargs)

        parent = parent or self.instance.parent

        self.fields['generation'].initial = parent.id
        self.fields['model'].initial = parent.parent.id
        self.fields['brand'].initial = parent.parent.parent.id
        self.fields['start_year'].initial = parent.attributes.years_of_production.start
        self.fields['end_year'].initial = parent.attributes.years_of_production.end

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

        self.add_field_group(
            'Параметры',
            [field for field in self.fields if field not in grouped_fields + self.parental_fields]
        )

        for field in self.fields:
            if field not in self.required:
                self.fields[field].required = False
                self[field].required = False

    def parental_form_content(self) -> list[Union[SafeString, str]]:
        """
        Получить содержание формы, относящееся к родителям конфигурации.
        :return: Содержание формы, список html-элементов.
        """
        columns = []
        for field in self.parental_fields:
            columns.append('<div class="col-lg-2 col-xs-12">')

            if self[field].label:
                columns.append(str(self[field].label_tag()))

            if self[field].help_text:
                columns.append(f'<div class="helptext">{{field.help_text | safe}}</div>')

            columns.append(str(self[field]))
            columns.append('</div>')

        return [
            Template(f'<h3>Сведения</h3>').render(Context({})),
            Template(f'<div class="row" style="margin-bottom: 20px;">{"".join(columns)}</div>').render(Context({})),
        ]

    def form_content(self, form_content=None, level=4) -> list[Union[SafeString, str]]:
        """
        Получить содержание формы.
        :param form_content: Из чего извлекать содержание формы.
        :param level: Уровень вложенности. Влияет на размер заголовков.
        :return: Содержание формы, список html-элементов.
        """
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
                form_content.append(
                    Template(f'<{tag} style="margin-top: {25 if level == 4 else 10}px">{legend}</{tag}>')
                    .render(Context({}))
                )

            if isinstance(content, list):
                tags = []
                for field in content:
                    tags.append('<div class="col-lg-2 col-xs-12">')

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
