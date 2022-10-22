from django.contrib import admin
from django.forms import ModelForm

from .proxy_models import Brand, VehicleModel, Generation

__all__ = ['VehicleModelAdmin']


#
# Модель.


class VehicleModelForm(ModelForm):
    class Meta:
        model = VehicleModel
        exclude = ['_type', 'description', 'attrs']
        labels = {
            'parent': 'Brand',
        }


class GenerationInlineForm(ModelForm):
    class Meta:
        model = Generation
        exclude = ['_type']


class GenerationInlineAdmin(admin.TabularInline):
    model = Generation
    extra = 0
    form = GenerationInlineForm


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    """Админка модели авто."""

    _type = VehicleModel.Type.MODEL

    form = VehicleModelForm
    inlines = [GenerationInlineAdmin]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(_type=self._type)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)

        form.base_fields['parent'].queryset = Brand.objects.filter(_type=Brand.Type.BRAND)
        form.base_fields['parent'].required = True

        return form

    def save_model(self, request, obj, form, change):
        obj._type = self._type
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance._type = Generation.Type.GENERATION
            instance.save()
        formset.save_m2m()
