from db_manager.models import Vehicle
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import TemplateView, View


class IndexView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        """
        Функция отображения для домашней страницы сайта.
        """
        return render(
            request,
            'index.html',
            context={
                'title': 'Главная страница',
                'data': Vehicle.objects.filter(_type=1),
                'type': '',
            }
        )


class BrandView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        """
        Функция отображения для домашней страницы сайта.
        """
        return render(
            request,
            'index.html',
            context={
                'title': 'Бренды',
                'data': Vehicle.objects.filter(_type=0),
                'type': '_brand',
            },
        )


class ModelView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        """
        Функция отображения для домашней страницы сайта.
        """
        return render(
            request,
            'index.html',
            context={
                'title': 'Модели',
                'data': Vehicle.objects.filter(_type=1),
                'type': '_model',
            },
        )


class GenerationView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        """
        Функция отображения для домашней страницы сайта.
        """
        return render(
            request,
            'index.html',
            context={
                'title': 'Поколения',
                'data': Vehicle.objects.filter(_type=2),
                'type': '_generation',
            },
        )


class RestylingView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        """
        Функция отображения для домашней страницы сайта.
        """
        return render(
            request,
            'index.html',
            context={
                'title': 'Рестайлинги',
                'data': Vehicle.objects.filter(_type=3),
                'type': '_restyling',
            },
        )


class ConfigurationView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        """
        Функция отображения для домашней страницы сайта.
        """
        return render(
            request,
            'index.html',
            context={
                'title': 'Комплектации',
                'data': Vehicle.objects.filter(_type=4),
                'type': '_configuration',
            },
        )
