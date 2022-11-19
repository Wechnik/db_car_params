from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from db_manager.models import Vehicle


class IndexView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        """
        Функция отображения для домашней страницы сайта.
        """
        return render(
            request,
            'index.html',
            context={'title': 'Главная страница', 'data': Vehicle.objects.filter(_type=1)}
        )
