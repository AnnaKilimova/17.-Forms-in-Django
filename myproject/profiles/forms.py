from django import forms # Классы и методы для создания и обработки форм.
from django.contrib.auth.models import User # Модель пользователя Django.
from django.core.exceptions import ValidationError # Стандартные исключения.
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm # Форма для смены пароля пользователя.

class RegistrationForm(forms.ModelForm):
    '''Форма регистрации.'''

    password = forms.CharField(widget=forms.PasswordInput) # Поле для ввода пароля пользователя.
    # forms.CharField — поле для текстовых данных (для пароля).
    # widget=forms.PasswordInput — Отображает вводимые данные как звездочки.

    password_confirm = forms.CharField(widget=forms.PasswordInput) # Поле для повторного ввода пароля.

    class Meta: # Имя встроенное.
        '''Для настройки поведения формы.'''

        model = User # Ссылка на модель, к которой привязывается форма. Встроенное имя.

        # Список полей модели, которые будут использоваться в форме. Встроенное имя.
        fields = ['username', 'email', 'password']
        # ['username', 'email', 'password'] — имена модели User, встроенные.

    def clean_password_confirm(self):
        '''Для проверки поля password_confirm.'''

        password = self.cleaned_data.get("password") # Получение очищенного значения поля password.
        password_confirm = self.cleaned_data.get("password_confirm") # Получение очищенного значения поля password_confirm.

        # Проверка на соответствие двух введенных паролей.
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match")
        return password_confirm

    def clean_username(self):
        '''Проверка уникальности имени пользователя.'''

        # Получение очищенного значения поля username.
        username = self.cleaned_data.get("username")

        # Проверка, существует ли пользователь с данным именем.
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username is already taken")
        return username

    # Проверка уникальности электронной почты.
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already taken")
        return email



class UserProfileForm(forms.ModelForm):
    '''Редактирование профиля.'''

    class Meta:
        '''Для настройки поведения формы.'''

        model = UserProfile
        fields = ['bio', 'birth_date', 'location', 'avatar']


class CustomPasswordChangeForm(PasswordChangeForm):
    '''Изменение пароля.'''

    def clean_new_password2(self):
        '''Для проверки подтверждения пароля нового пароля.'''

        new_password = self.cleaned_data.get("new_password1")
        old_password = self.cleaned_data.get("old_password")

        # Проверка, что новый пароль не совпадает с текущим.
        if new_password == old_password:
            raise forms.ValidationError("The new password must be different from the current password.")
        return new_password


