from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/accounts/login/')
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    return render(
        request,
        'index.html',
        context={'title': 'Главная страница'}
    )
