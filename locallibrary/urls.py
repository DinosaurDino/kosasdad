"""
Конфигурация URL-адреса локальной библиотеки

Список `urlpatterns` направляет URL-адреса в представления. Для получения дополнительной информации см.:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Примеры:
Представления функций
    1. Добавьте импорт: из представлений импорта my_app
    2. Добавьте URL-адрес в шаблоны URL-адресов: url(r'^$', views.home, name='home')
Представления на основе классов
    1. Добавьте импорт: from other_app.views import Home
    2. Добавьте URL-адрес в шаблоны URL-адресов: url(r'^$', Home.as_view(), name='home')
Включение другой конфигурации URL
    1. Импортируйте функцию include(): из django.conf.urls импортируйте URL-адрес, включите
    2. Добавьте URL-адрес в шаблоны URL-адресов: url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin

# Используйте include() чтобы добавлять URL из каталога приложения
from django.urls import include
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('catalog/', include('catalog.urls')),
]

# Используйте static() чтобы добавить соотношения для статических файлов
# Только на период разработки
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Добавьте URL соотношения, чтобы перенаправить запросы с корневого URL, на URL приложения
from django.views.generic import RedirectView

urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
