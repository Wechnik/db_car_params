from django.views.generic import UpdateView

from db_manager.views import BaseLoginRequiredMixin


# class ConfigurationUpdateView(BaseLoginRequiredMixin, UpdateView):
#     form_class = ConfigurationForm
#     template_name = 'configuration/create.html'
#     queryset = Vehicle.objects.all()