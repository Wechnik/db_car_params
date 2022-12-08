__all__ = [
    'IndexView',
    'BrandView',
    'ModelView',
    'GenerationView',
    'ConfigurationView',
]

from db_manager.models import Vehicle
from django.shortcuts import render
from django.views.generic.base import View

from db_manager.views.abstract import BaseLoginRequiredMixin


class IndexView(BaseLoginRequiredMixin, View):
    """Представление главной страницы."""

    def get(self, request, *args, **kwargs):
        """Метод отображения для домашней страницы сайта."""

        data = Vehicle.objects.filter(_type=2)
        structure_data = []
        for item in data:
            structure_data.append(item.get_structured_data())

        return render(
            request,
            'main.html',
            context={
                'title': 'Главная страница',
                'data': structure_data,
                'type': '',
            }
        )


class BrandView(BaseLoginRequiredMixin, View):
    """Представление страницы брендов."""

    def get(self, request, *args, **kwargs):
        """Метод отображения для брендов авто."""
        return render(
            request,
            'index.html',
            context={
                'title': 'Бренды',
                'data': Vehicle.objects.filter(_type=0),
                'type': '_brand',
            },
        )


class ModelView(BaseLoginRequiredMixin, View):
    """Представление страницы моделей."""

    def get(self, request, *args, **kwargs):
        """Метод отображения для моделей авто."""
        return render(
            request,
            'index.html',
            context={
                'title': 'Модели',
                'data': Vehicle.objects.filter(_type=1),
                'type': '_model',
            },
        )


class GenerationView(BaseLoginRequiredMixin, View):
    """Представление страницы поколений."""

    def get(self, request, *args, **kwargs):
        """Метод отображения для поколений авто."""
        return render(
            request,
            'index.html',
            context={
                'title': 'Поколения',
                'data': Vehicle.objects.filter(_type=2),
                'type': '_generation',
            },
        )


class ConfigurationView(BaseLoginRequiredMixin, View):
    """Представление страницы комплектаций."""

    def get(self, request, *args, **kwargs):
        """Метод отображения для комплектаций авто."""
        return render(
            request,
            'index.html',
            context={
                'title': 'Комплектации',
                'data': Vehicle.objects.filter(_type=3),
                'type': '_configuration',
            },
        )
