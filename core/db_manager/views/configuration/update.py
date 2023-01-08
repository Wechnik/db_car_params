from django.urls import reverse
from django.views.generic import UpdateView

from db_manager.forms.configuration import ConfigurationForm
from db_manager.models import Vehicle
from db_manager.views.abstract import BaseLoginRequiredMixin


class ConfigurationUpdateView(BaseLoginRequiredMixin, UpdateView):
    form_class = ConfigurationForm
    template_name = 'configuration/create.html'
    queryset = Vehicle.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        gen = self.object.parent
        context['generation'] = gen

        # Комплектации будут отсортированы по возрастанию даты начала выпуска.
        # Комплектации, у которых даты производства совпадают, будут отсортированы по дате конца выпуска.
        config_list = sorted(
            list(Vehicle.objects.filter(parent=gen.id)),
            key=lambda cfg: (
                float('inf') if cfg.attributes.years_of_production.start is None
                else cfg.attributes.years_of_production.start,
                float('inf') if cfg.attributes.years_of_production.end is None
                else cfg.attributes.years_of_production.end,
            )
        )

        # Нет ни одной комплектации. Информацией о базовой комплектации является информация о поколении.
        if not config_list:
            current_config = self.object
            current_config.name = 'Базовая комплектация'
            config_list = [current_config]

        # Указываем какая комплектация будет отображена по умолчанию. Если нет предпочтений - выбираем первую.
        for config in config_list:
            if self.object.id == config.id:
                config.selected = True
                break
        else:
            config_list[0].selected = True

        # Нужна для отображения списка доступных комплектаций и информации о самих комплектациях.
        context['config_list'] = config_list

        context['title'] = gen

        return context

    def get_success_url(self):
        return reverse('edit_configuration', kwargs={'pk': self.object.id})
