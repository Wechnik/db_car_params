from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View


class Index(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        """
        Функция отображения для домашней страницы сайта.
        """
        return render(
            request,
            'index.html',
            context={'title': 'Главная страница'}
        )
