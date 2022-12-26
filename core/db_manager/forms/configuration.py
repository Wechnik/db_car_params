from db_manager.forms.core import cleaned_data_to_json, YearsOfProduction, WiperLength, OilType, RimOffset, \
    RimCenterHoleDiameter, RimDiameter, RimDrilling, RimWidth, TireDiameter, TireHeight, TireWidth
from db_manager.forms.crud_forms import BaseVehicleForm
from db_manager.models import Vehicle
from db_manager.models.vehicle.attributes import Attributes


class ConfigurationForm(BaseVehicleForm,
                        RimDiameter, RimDrilling, RimWidth, RimCenterHoleDiameter, RimOffset,
                        TireDiameter, TireWidth, TireHeight,
                        WiperLength,
                        OilType,
                        YearsOfProduction):
    class Meta:
        model = Vehicle
        fields = ['name', 'description']
        labels = {
            'name': 'Название',
            'description': 'Описание',
        }

    template_name_div = 'div.html'

    def save(self, commit=True):
        self.instance.attributes = Attributes.from_json(cleaned_data_to_json(self.cleaned_data).get('attributes'))
        return super().save(commit=commit)

    def __init__(self, *args, **kwargs):
        BaseVehicleForm.__init__(self, *args, **kwargs)

        for base_type in type(self).mro():
            if hasattr(base_type, 'fill_initial'):
                base_type.fill_initial(self)
