from django.contrib import admin
from django.forms import ModelForm

from .proxy_models import Configuration, Restyling

__all__ = ['ConfigurationAdmin']


#
# Комплектация.


class ConfigurationForm(ModelForm):
    class Meta:
        model = Configuration
        exclude = ['_type']
        labels = {
            'parent': 'Restyling',
        }


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    _type = Restyling.Type.CONFIGURATION

    form = ConfigurationForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(_type=Configuration.Type.CONFIGURATION)

    def save_model(self, request, obj, form, change):
        obj._type = self._type
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)

        form.base_fields['parent'].queryset = Restyling.objects.filter(_type=Restyling.Type.RESTYLING)
        form.base_fields['parent'].required = True

        return form
