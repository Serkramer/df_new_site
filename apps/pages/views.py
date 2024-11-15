from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.pages.forms import ProfileForm
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


class ProfileView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context
