from django.urls.conf import path, include

from db_manager.views import Index

urlpatterns = [
    path('', Index.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
]
