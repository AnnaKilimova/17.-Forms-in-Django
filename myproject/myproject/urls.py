from django.contrib import admin
from django.urls import include, path

# Подключение маршрутовю
urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', include('profiles.urls')),
]
