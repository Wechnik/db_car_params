from django.contrib.auth.views import LoginView
from django.shortcuts import render


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        # context={},
    )


