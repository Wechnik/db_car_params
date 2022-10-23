from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, ListView
from db_manager.models import Vehicle
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


class BasicUsageListingView(ListView):
    template_name = 'vehicle.html'
    extra_context = dict(employees_as_model=Vehicle)  # See 'Employee' definition in "Read me first" at home page.
