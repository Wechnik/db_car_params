from django.contrib import admin
from django.forms import ModelForm, IntegerField

from .proxy_models import Generation, Restyling, VehicleModel

__all__ = ['GenerationAdmin']


#
# Поколение.


class GenerationForm(ModelForm):
    class Meta:
        model = Generation
        exclude = ['_type']
        labels = {
            'parent': 'Model',
        }


class RestylingInlineForm(ModelForm):
    class Meta:
        model = Restyling
        exclude = ['_type']


class RestylingInlineAdmin(admin.TabularInline):
    model = Restyling
    extra = 0
    form = RestylingInlineForm


@admin.register(Generation)
class GenerationAdmin(admin.ModelAdmin):
    _type = Restyling.Type.GENERATION

    form = GenerationForm
    inlines = [RestylingInlineAdmin]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(_type=self._type)

    def save_model(self, request, obj, form, change):
        obj._type = self._type
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)

        form.base_fields['parent'].queryset = VehicleModel.objects.filter(_type=VehicleModel.Type.MODEL)
        form.base_fields['parent'].required = True

        return form

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance._type = VehicleModel.Type.RESTYLING
            instance.save()
        formset.save_m2m()
