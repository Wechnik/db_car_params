from django.db.models import QuerySet
from django.http import HttpResponseRedirect, QueryDict
from django.urls import reverse
from django.views.generic import UpdateView

from db_manager.forms.configuration import ConfigurationForm
from db_manager.models import Vehicle
from db_manager.views.abstract import BaseLoginRequiredMixin


class ConfigurationUpdateView(BaseLoginRequiredMixin, UpdateView):
    form_class = ConfigurationForm
    template_name = 'configuration/create.html'
    queryset = Vehicle.objects.all()

    def post(self, request, *args, **kwargs):
        # Для полей, связанных с задними колесами/дисками приходит несколько значений.
        # Первое - действительное, второе - пустое. Почему - непонятно. Для передних все ок.
        # QueryDict работает таким образом, что если значений несколько - берет последнее.
        # Получается, что всегда берется пустое. Это временный костыль - вручную берем первое, пока не исправим причину.
        query_dict = QueryDict(mutable=True)
        query_dict.update({
            key: values[0]
            for key, values in dict(request.POST).items()
        })
        request.POST = query_dict
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except IndexError:
            return HttpResponseRedirect(reverse('add_configuration', kwargs={'pk': self.kwargs['pk']}))

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj._type == Vehicle.Type.GENERATION:
            obj = self.get_sorted_config_list(obj)[0]
        return obj

    @staticmethod
    def get_sorted_config_list(gen: Vehicle) -> QuerySet:
        return Vehicle.objects.filter(parent=gen.id).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        gen = self.object.parent
        context['generation'] = gen

        # Комплектации будут отсортированы по возрастанию даты начала выпуска.
        # Комплектации, у которых даты производства совпадают, будут отсортированы по дате конца выпуска.
        config_list = self.get_sorted_config_list(gen)

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
