from django.contrib import admin
from django.forms import ModelForm

from .proxy_models import Brand, VehicleModel

__all__ = ['BrandAdmin']


#
# Производитель.


class BrandForm(ModelForm):
    class Meta:
        model = Brand
        exclude = ['parent', '_type', 'description', 'attrs']


class VehicleModelInlineForm(ModelForm):
    class Meta:
        model = VehicleModel
        exclude = ['_type']


class VehicleModelInlineAdmin(admin.TabularInline):
    model = VehicleModel
    extra = 0
    form = VehicleModelInlineForm


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    _type = Brand.Type.BRAND

    form = BrandForm
    inlines = [VehicleModelInlineAdmin]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(_type=self._type)

    def save_model(self, request, obj, form, change):
        obj._type = self._type
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance._type = VehicleModel.Type.MODEL
            instance.save()
        formset.save_m2m()
