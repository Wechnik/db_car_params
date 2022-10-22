from django.contrib import admin
from django.forms import ModelForm

from .proxy_models import Restyling, Configuration

__all__ = ['RestylingAdmin']


#
# Рестайлинг.

class RestylingForm(ModelForm):
    class Meta:
        model = Restyling
        exclude = ['_type']
        labels = {
            'parent': 'Generation',
        }


class ConfigurationInlineForm(ModelForm):
    class Meta:
        model = Configuration
        exclude = ['_type']


class ConfigurationInlineAdmin(admin.TabularInline):
    model = Configuration
    extra = 0
    form = ConfigurationInlineForm


@admin.register(Restyling)
class RestylingAdmin(admin.ModelAdmin):
    _type = Restyling.Type.RESTYLING

    form = RestylingForm
    inlines = [ConfigurationInlineAdmin]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(_type=self._type)

    def save_model(self, request, obj, form, change):
        obj._type = self._type
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)

        form.base_fields['parent'].queryset = Restyling.objects.filter(_type=Restyling.Type.GENERATION)
        form.base_fields['parent'].required = True

        return form

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance._type = Configuration.Type.CONFIGURATION
            instance.save()
        formset.save_m2m()

