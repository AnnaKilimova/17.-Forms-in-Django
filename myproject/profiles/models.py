# Обращение к модулю БД Django, который содержит инструменты для работы с моделями и полями.
from django.db import models # models — отвечает за описание структур данных (моделей).
# Для работы с пользователями (авторизация и аутентификация).
from django.contrib.auth.models import User # User — модель пользователя.


class UserProfile(models.Model):
    '''
    Модель профиля пользователя в БД.
    models.Model: базовые методы и свойства для работы с данными.
    '''

    # user — Ссылка на объект User к которому привязывается профиль.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # models.OneToOneField — встроенный тип связи, связывает каждый профиль с единственным пользователем.
    # on_delete=models.CASCADE — при удалении пользователя (User) должен удаляться и связанный профиль (UserProfile).

    # Поле для хранения биографической информации пользователя.
    bio = models.TextField(max_length=500, blank=True)
    # models.TextField — тип поля для хранения длинного текста.
    # max_length=500 — максимальная длина текста.
    # blank=True — поле м.б. пустым при создании или редактировании записи.

    # Поле для хранения даты рождения.
    birth_date = models.DateField(null=True, blank=True)
    # models.DateField — Тип поля для хранения даты.
    # null=True — допускается хранение NULL значений в БД.
    # blank=True — поле м.б. пустым при заполнении формы.

    # Поле для хранения местоположения пользователя.
    location = models.CharField(max_length=30, blank=True)
    # models.CharField — тип поля для хранения коротких строк.
    # max_length=30 — максимальная длина строки.
    # blank=True — поле м.б. пустым.

    # Поле для хранения аватара пользователя.
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    # models.ImageField — тип поля для хранения изображений.
    # upload_to='avatars/' — путь, по которому будут сохраняться загруженные изображения
    # (папка avatars/ в корневом каталоге медиафайлов).
    # blank=True — допускается пустое значение в форме.
    # null=True — допускается NULL в БД.

    def __str__(self):
        return self.user.username # Возвращает имя пользователя, к которому привязан профиль.

