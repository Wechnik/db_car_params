from typing import Union

from django.forms import ModelChoiceField, Select, BooleanField, CheckboxInput
from django.template import Template, Context
from django.utils.safestring import SafeString

from db_manager.forms.core import cleaned_data_to_json, get_model_choice_field, get_model_choice_field_queryset, Sorter
from db_manager.forms.crud_forms import BaseVehicleForm
from db_manager.helpers import deepget, deepdel
from db_manager.models import Vehicle, ParamsValue
from db_manager.models.vehicle.attributes import Attributes


class VehicleSelect(Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, value.instance.name if value else value, selected, index, subindex,
                                       attrs)
        if value:
            children = Vehicle.objects.filter(parent=value.instance.id)
            if children:
                option['attrs']['data-children'] = ','.join([str(child.id) for child in children])
        return option


class ParamSelect(Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, value.instance.value if value else value, selected, index, subindex,
                                       attrs)
        if value:
            children = value.instance.child.all()
            if children:
                option['attrs']['data-children'] = ','.join([str(child.id) for child in children])

        return option


def get_id_from_obj(obj):
    return obj.id if obj is not None else None


class ConfigurationForm(BaseVehicleForm):
    brand = ModelChoiceField(
        label='Брэнд',
        queryset=Vehicle.objects.filter(_type=Vehicle.Type.BRAND.value),
        to_field_name='id',
        required=True,
        widget=VehicleSelect(attrs={'onChange': 'onSelectChange(this);', 'data-child': 'model'}),
    )
    model = ModelChoiceField(
        label='Модель',
        queryset=Vehicle.objects.filter(_type=Vehicle.Type.MODEL.value),
        to_field_name='id',
        required=True,
        widget=VehicleSelect(attrs={'onChange': 'onSelectChange(this);', 'data-child': 'generation'})
    )
    generation = ModelChoiceField(
        label='Поколение',
        queryset=Vehicle.objects.filter(_type=Vehicle.Type.GENERATION.value),
        to_field_name='id',
        required=True,
        widget=VehicleSelect(),
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

    # Диски

    attributes__restrictions__rim__drilling__rec = ModelChoiceField(
        label='Сверловка',
        queryset=get_model_choice_field_queryset(ParamsValue.Type.WHEEL_DRILLING, Sorter.sort_drilling),
        to_field_name='id',
        widget=ParamSelect(attrs={
            'onChange': 'onSelectChange(this);',
            'data-child': 'attributes__restrictions__rim__diameter__rec'
        })
    )

    attributes__restrictions__rim__diameter__rec = ModelChoiceField(
        label='Диаметр',
        queryset=get_model_choice_field_queryset(ParamsValue.Type.WHEEL_DIAMETER, Sorter.sort_diameter),
        to_field_name='id',
        widget=ParamSelect(attrs={
            'onChange': 'onSelectChange(this);',
            'data-child': 'attributes__restrictions__rim__width__rec'
        })
    )

    attributes__restrictions__rim__width__rec = ModelChoiceField(
        label='Ширина',
        queryset=get_model_choice_field_queryset(ParamsValue.Type.WHEEL_WIDTH, Sorter.sort_number),
        to_field_name='id',
        widget=ParamSelect(attrs={'onChange': 'onSelectChange(this);'})
    )

    attributes__restrictions__rim__offset__rec = get_model_choice_field(
        get_model_choice_field_queryset(ParamsValue.Type.WHEEL_DEPARTURE, Sorter.sort_number),
        'Вынос'
    )

    attributes__restrictions__rim__center_hole_diameter__rec = get_model_choice_field(
        get_model_choice_field_queryset(ParamsValue.Type.WHEEL_CH_DIAMETER, Sorter.sort_number),
        'Диаметр ЦО'
    )

    attributes__restrictions__different_rims = BooleanField(
        label='Разные размеры',
        widget=CheckboxInput(attrs={
            'onChange': 'toggleHideClass(this, "rearRims");'
        })
    )

    attributes__restrictions__rear_rim__drilling__rec = ModelChoiceField(
        label='Сверловка',
        queryset=get_model_choice_field_queryset(ParamsValue.Type.WHEEL_DRILLING, Sorter.sort_drilling),
        to_field_name='id',
        widget=ParamSelect(attrs={
            'onChange': 'onSelectChange(this);',
            'data-child': 'attributes__restrictions__rear_rim__diameter__rec'
        })
    )

    attributes__restrictions__rear_rim__diameter__rec = ModelChoiceField(
        label='Диаметр',
        queryset=get_model_choice_field_queryset(ParamsValue.Type.WHEEL_DIAMETER, Sorter.sort_diameter),
        to_field_name='id',
        widget=ParamSelect(attrs={
            'onChange': 'onSelectChange(this);',
            'data-child': 'attributes__restrictions__rear_rim__width__rec'
        })
    )

    attributes__restrictions__rear_rim__width__rec = ModelChoiceField(
        label='Ширина',
        queryset=get_model_choice_field_queryset(ParamsValue.Type.WHEEL_WIDTH, Sorter.sort_number),
        to_field_name='id',
        widget=ParamSelect(attrs={'onChange': 'onSelectChange(this);'})
    )

    attributes__restrictions__rear_rim__offset__rec = get_model_choice_field(
        get_model_choice_field_queryset(ParamsValue.Type.WHEEL_DEPARTURE, Sorter.sort_number),
        'Вынос'
    )

    attributes__restrictions__rear_rim__center_hole_diameter__rec = get_model_choice_field(
        get_model_choice_field_queryset(ParamsValue.Type.WHEEL_CH_DIAMETER, Sorter.sort_number),
        'Диаметр ЦО'
    )

    # Шины

    attributes__restrictions__tire__diameter__rec = ModelChoiceField(
        label='Диаметр',
        queryset=get_model_choice_field_queryset(ParamsValue.Type.TIRE_DIAMETER, Sorter.sort_number),
        to_field_name='id',
        widget=ParamSelect(attrs={
            'onChange': 'onSelectChange(this);',
            'data-child': 'attributes__restrictions__tire__width__rec'
        })
    )

    attributes__restrictions__tire__width__rec = ModelChoiceField(
        label='Ширина',
        queryset=get_model_choice_field_queryset(ParamsValue.Type.TIRE_METRIC_WIDTH, Sorter.sort_number),
        to_field_name='id',
        widget=ParamSelect(attrs={'onChange': 'onSelectChange(this);'})
    )

    attributes__restrictions__tire__height__rec = get_model_choice_field(
        get_model_choice_field_queryset(ParamsValue.Type.TIRE_INCH_HEIGHT, Sorter.sort_number),
        'Высота профиля, %'
    )

    attributes__restrictions__different_tires = BooleanField(
        label='Разные размеры',
        widget=CheckboxInput(attrs={
            'onChange': 'toggleHideClass(this, "rearTires");'
        })
    )

    attributes__restrictions__rear_tire__diameter__rec = ModelChoiceField(
        label='Диаметр',
        queryset=get_model_choice_field_queryset(ParamsValue.Type.TIRE_DIAMETER, Sorter.sort_number),
        to_field_name='id',
        widget=ParamSelect(attrs={
            'onChange': 'onSelectChange(this);',
            'data-child': 'attributes__restrictions__rear_tire__width__rec'
        })
    )

    attributes__restrictions__rear_tire__width__rec = ModelChoiceField(
        label='Ширина',
        queryset=get_model_choice_field_queryset(ParamsValue.Type.TIRE_METRIC_WIDTH, Sorter.sort_number),
        to_field_name='id',
        widget=ParamSelect(attrs={'onChange': 'onSelectChange(this);'})
    )

    attributes__restrictions__rear_tire__height__rec = get_model_choice_field(
        get_model_choice_field_queryset(ParamsValue.Type.TIRE_INCH_HEIGHT, Sorter.sort_number),
        'Высота профиля, %'
    )

    # Дворник

    attributes__restrictions__wiper__length__rec = get_model_choice_field(
        get_model_choice_field_queryset(ParamsValue.Type.WIPERS_LENGTH, Sorter.sort_number),
        'Длина, мм'
    )

    # Масло

    attributes__restrictions__oil__type = get_model_choice_field(
        get_model_choice_field_queryset(ParamsValue.Type.OIL_TYPE),
        'Тип'
    )

    attributes__restrictions__oil__viscosity = get_model_choice_field(
        get_model_choice_field_queryset(ParamsValue.Type.OIL_VISCOSITY),
        'Вязкость'
    )

    # Аккумулятор

    attributes__restrictions__battery__capacity = get_model_choice_field(
        get_model_choice_field_queryset(ParamsValue.Type.BATTERY_CAPACITY, Sorter.sort_number),
        'Емкость'
    )

    attributes__restrictions__battery__polarity = get_model_choice_field(
        get_model_choice_field_queryset(ParamsValue.Type.BATTERY_POLARITY),
        'Полярность'
    )

    attributes__restrictions__battery__dimensions = get_model_choice_field(
        get_model_choice_field_queryset(ParamsValue.Type.BATTERY_DIMENSIONS),
        'Габариты'
    )

    attributes__restrictions__battery__starting_current = get_model_choice_field(
        get_model_choice_field_queryset(ParamsValue.Type.BATTERY_STARTING_CURRENT, Sorter.sort_number),
        'Пусковой ток'
    )

    class Meta:
        model = Vehicle
        fields = ['name', 'description']
        labels = {
            'name': 'Название',
            'description': 'Описание',
        }

    required = ('name', 'brand', 'model', 'generation')

    template_name_div = 'configuration/div.html'

    def clean(self):
        super().clean()
        for field, value in self.cleaned_data.items():
            if isinstance(value, ParamsValue):
                self.cleaned_data[field] = value.id

        return self.cleaned_data

    def save(self, commit=True):
        attributes = cleaned_data_to_json(self.cleaned_data).get('attributes')
        if not deepget(attributes, ['restrictions', 'different_rims']):
            deepdel(attributes, ['restrictions', 'rear_rim'])

        if not deepget(attributes, ['restrictions', 'different_tires']):
            deepdel(attributes, ['restrictions', 'rear_tire'])

        self.instance.attributes = Attributes.from_json(attributes)

        self.instance.parent = self.cleaned_data.get('generation')
        self.instance.parent.parent = self.cleaned_data.get('model')
        self.instance.parent.attributes.years_of_production.start = self.cleaned_data.get('start_year')
        self.instance.parent.attributes.years_of_production.end = self.cleaned_data.get('end_year')
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

        attribute_fields = [
            'attributes__restrictions__oil__type',
            'attributes__restrictions__oil__viscosity',
            'attributes__restrictions__wiper__length__rec',
            'attributes__restrictions__tire__diameter__rec',
            'attributes__restrictions__tire__height__rec',
            'attributes__restrictions__tire__width__rec',
            'attributes__restrictions__rim__offset__rec',
            'attributes__restrictions__rim__center_hole_diameter__rec',
            'attributes__restrictions__rim__diameter__rec',
            'attributes__restrictions__rim__drilling__rec',
            'attributes__restrictions__rim__width__rec',
            'attributes__restrictions__different_rims',
            'attributes__restrictions__rear_rim__drilling__rec',
            'attributes__restrictions__rear_rim__diameter__rec',
            'attributes__restrictions__rear_rim__width__rec',
            'attributes__restrictions__rear_rim__offset__rec',
            'attributes__restrictions__rear_rim__center_hole_diameter__rec',
            'attributes__restrictions__different_tires',
            'attributes__restrictions__rear_tire__diameter__rec',
            'attributes__restrictions__rear_tire__width__rec',
            'attributes__restrictions__rear_tire__height__rec',
            'attributes__restrictions__battery__capacity',
            'attributes__restrictions__battery__polarity',
            'attributes__restrictions__battery__dimensions',
            'attributes__restrictions__battery__starting_current',
        ]
        for attribute_field in attribute_fields:
            self.fields[attribute_field].initial = deepget(self.instance.attrs, attribute_field.split('__')[1:])

        for base_type in type(self).mro():
            if hasattr(base_type, 'fill_initial'):
                base_type.fill_initial(self)

        def NestedDictValues(d):
            for v in d.values():
                if isinstance(v, dict):
                    yield from NestedDictValues(v)
                elif isinstance(v, tuple):
                    yield v[1]
                else:
                    yield v

        self.field_groups = {
            'Диски': [
                'attributes__restrictions__rim__drilling__rec',
                'attributes__restrictions__rim__diameter__rec',
                'attributes__restrictions__rim__width__rec',
                'attributes__restrictions__rim__offset__rec',
                'attributes__restrictions__rim__center_hole_diameter__rec',
                'attributes__restrictions__different_rims',
            ],
            ('Задние диски', 'rearRims'): (
                'rearRims',
                [
                    'attributes__restrictions__rear_rim__drilling__rec',
                    'attributes__restrictions__rear_rim__diameter__rec',
                    'attributes__restrictions__rear_rim__width__rec',
                    'attributes__restrictions__rear_rim__offset__rec',
                    'attributes__restrictions__rear_rim__center_hole_diameter__rec',
                ]
            ),
            'Шины': [
                'attributes__restrictions__tire__diameter__rec',
                'attributes__restrictions__tire__width__rec',
                'attributes__restrictions__tire__height__rec',
                'attributes__restrictions__different_tires',
            ],
            ('Задние шины', 'rearTires'): (
                'rearTires',
                [
                    'attributes__restrictions__rear_tire__diameter__rec',
                    'attributes__restrictions__rear_tire__width__rec',
                    'attributes__restrictions__rear_tire__height__rec',
                ]
            ),
            'Дворник': [
                'attributes__restrictions__wiper__length__rec',
            ],
            'Масло': [
                'attributes__restrictions__oil__viscosity',
                'attributes__restrictions__oil__type',
            ],
            'Аккумулятор': [
                'attributes__restrictions__battery__capacity',
                'attributes__restrictions__battery__polarity',
                'attributes__restrictions__battery__dimensions',
                'attributes__restrictions__battery__starting_current',
            ]
        }

        grouped_fields = []
        for field_group in NestedDictValues(self.field_groups):
            grouped_fields.extend(field_group)

        self.field_groups['Параметры'] = [
            field for field in self.fields if field not in grouped_fields + self.parental_fields
        ]

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
                legend_class = None
                if isinstance(legend, tuple):
                    legend, legend_class = legend

                legend_class_str = f'class="{legend_class}"' if legend_class else ''

                tag = levels[level]
                form_content.append(
                    Template(f'<{tag} {legend_class_str} style="margin-top: {25 if level == 4 else 10}px">{legend}</{tag}>')
                    .render(Context({}))
                )

            if isinstance(content, (tuple, list)):
                content_classes = ['row']
                if isinstance(content, tuple):
                    content_class, content = content
                    content_classes.append(content_class)

                content_class_str = f'class="{" ".join(content_classes)}"'

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
                    Template(f'<div {content_class_str}>{"".join([wrapped_field for wrapped_field in wrapped_fields])}</div>')
                    .render(Context({}))
                )
            else:
                form_content.extend(self.form_content(content, level + 1))

        return form_content
