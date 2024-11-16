from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from apps.pages.forms import ProfileForm, CustomPasswordChangeForm
from auth.models import Profile
from web_project import TemplateLayout
from django.views.generic.edit import FormMixin

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to pages/urls.py file for more pages.
"""


class PagesView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


@method_decorator(login_required, name='dispatch')
class AccountSettingsView(TemplateView):
    template_name = "pages_account_settings_account.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        profile = get_object_or_404(Profile, user=self.request.user)
        form = ProfileForm(instance=profile)  # Предзаполнение формы данными профиля
        context['profile_form'] = form
        context['title'] = 'Налаштування акаунту'
        return context

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=self.request.user)
        form = ProfileForm(request.POST, instance=profile)  # Связываем форму с профилем пользователя
        if form.is_valid():
            form.save()  # Сохраняем изменения в профиле
            return HttpResponseRedirect(self.request.path)  # Перенаправляем на текущую страницу
        else:
            context = self.get_context_data()
            context['profile_form'] = form
            return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
class UpdateAvatarView(View):
    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        avatar = request.FILES.get('avatar')

        if avatar:
            # Проверка размера файла (2 MB = 2 * 1024 * 1024 байта)
            max_file_size = 2 * 1024 * 1024
            if avatar.size > max_file_size:
                return JsonResponse({'error': 'Файл перевищує максимальний розмір 2 MB'}, status=400)

            # Проверка формата файла
            allowed_formats = ['image/jpeg', 'image/png']
            if avatar.content_type not in allowed_formats:
                return JsonResponse({'error': 'Непідтримуваний формат файлу. Дозволені формати: JPG, PNG.'}, status=400)

            # Сохраняем аватар
            profile.avatar = avatar
            profile.save()
            return JsonResponse({'avatar_url': profile.avatar.url}, status=200)

        return JsonResponse({'error': 'Файл не завантажено'}, status=400)


class ChangePasswordView(FormView):
    template_name = "pages_account_settings_security.html"
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('pages-account-settings-security')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['title'] = 'Налаштування акаунту'
        return context


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)  # Чтобы не разлогинивать пользователя
        messages.success(self.request, "Пароль успішно змінено!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Виправте помилки у формі.")
        return super().form_invalid(form)


class ProfileView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context
