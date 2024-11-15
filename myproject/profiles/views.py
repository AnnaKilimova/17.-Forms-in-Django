# Для отображения сообщений пользователю (успешных уведомлений или ошибок).
from django.contrib import messages
# login — для входа пользователя в систему.
# authenticate — для проверки аутентификационных данных пользователя.
# update_session_auth_hash — встроенная функция, которая обновляет хеш сессии пользователя,
# чтобы не разлогинить его после смены пароля.
from django.contrib.auth import login, authenticate, update_session_auth_hash
# Встроенный декоратор, требующий, чтобы пользователь был аутентифицирован для доступа к представлению.
from django.contrib.auth.decorators import login_required
# Для рендеринга HTML-шаблона и передачи в него данных, и перенаправления пользователя на другую страницу соответсвенно
from django.shortcuts import render, redirect

from .forms import RegistrationForm, UserProfileForm, CustomPasswordChangeForm
from .models import UserProfile


def register_view(request):
    '''Функция представления для регистрации пользователя.'''

    # Встроенное свойство объекта request, указывающее метод запроса (POST или GET).
    if request.method == 'POST':
        # Создание экземпляра формы с переданными POST-данными.
        form = RegistrationForm(request.POST)
        if form.is_valid(): # Метод, встроенный в Django формы, проверяет правильность введенных данных.
            # Сохранение формы без записи в БД (чтобы добавить дополнительные данные перед окончательным сохранением).
            user = form.save(commit=False)

            # set_password — метод, встроенный в Django для безопасного хеширования пароля.
            # form.cleaned_data['password'] — доступ к очищенным данным формы.
            user.set_password(form.cleaned_data['password'])

            user.save() # Сохранение пользователя в БД.

            UserProfile.objects.create(user=user) # Создание связанного профиля для нового пользователя.
            login(request, user) # Выполнение входа для вновь зарегистрированного пользователя.
            return redirect('profile') # Перенаправление пользователя на страницу профиля после регистрации.

    else:
        form = RegistrationForm() # Создание пустой формы, если метод запроса не POST.
    # Рендеринг шаблона register.html с передачей формы в контексте.
    return render(request, 'profiles/register.html', {'form': form})

@login_required
def edit_profile_view(request):
    '''Представление для редактирования профиля пользователя.'''

    # Доступ к профилю пользователя через поле userprofile модели User.
    user_profile = request.user.userprofile
    if request.method == 'POST':

        # Создание формы UserProfileForm с данными из POST-запроса и файлами.
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save() # Сохранение отредактированного профиля.
            messages.success(request, "Profile updated successfully") # Добавление успешного сообщения.
            return redirect('profile') # Перенаправление на страницу профиля.

    else:
        # Создание формы для редактирования профиля с текущими данными пользователя.
        form = UserProfileForm(instance=user_profile)
    # Рендеринг шаблона с формой редактирования профиля.
    return render(request, 'profiles/edit_profile.html', {'form': form})

@login_required
def change_password_view(request):
    # Для смены пароля пользователя.
    if request.method == 'POST':
        # Создание формы смены пароля с данными POST-запроса.
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save() # Сохранение нового пароля.
            update_session_auth_hash(request, user) # Обновление сессии пользователя после смены пароля.
            messages.success(request, "Password changed successfully")
            return redirect('profile')
    else:
        # Создание формы смены пароля без данных.
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'profiles/change_password.html', {'form': form})

@login_required
def profile_view(request):
    '''Отображение профиля пользователя.'''
    return render(request, 'profiles/profile.html', {'user_profile': request.user.userprofile})
