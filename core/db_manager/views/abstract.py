from django.contrib.auth.mixins import LoginRequiredMixin


class BaseLoginRequiredMixin(LoginRequiredMixin):
    """Базовый класс для запрета на неавторизованный вход."""

    login_url = '/accounts/login/'
