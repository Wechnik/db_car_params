__all__ = ['VehicleDetailView']

from db_manager.models import Vehicle
from db_manager.views.detail import BaseVehicleDetailView


class VehicleDetailView(BaseVehicleDetailView):
    template_name = 'all_car/detail.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.preferred_config = None

    def get(self, request, *args, **kwargs):
        self.preferred_config = kwargs.get('cfg_pk')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Нужна для редиректа на страницу добавления конфигураций поколения.
        context['generation'] = self.object

        # Комплектации будут отсортированы по возрастанию даты начала выпуска.
        # Комплектации, у которых даты производства совпадают, будут отсортированы по дате конца выпуска.
        config_list = sorted(
            list(Vehicle.objects.filter(parent=context['vehicle'].id)),
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
        if not self.preferred_config:
            config_list[0].selected = True
        else:
            for config in config_list:
                if self.preferred_config == config.id:
                    config.selected = True
                    break
            else:
                config_list[0].selected = True

        # Нужна для отображения списка доступных комплектаций и информации о самих комплектациях.
        context['config_list'] = config_list

        return context
