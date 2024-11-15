from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

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
class AccountSettingsView(TemplateView, FormMixin):

    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        profile = get_object_or_404(Profile, user=self.request.user)
        context['title'] = 'Налаштування акаунту'
        context['profile_form'] = self.get_form()
        context['profile'] = profile
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()  # Сохранение данных формы
            return HttpResponseRedirect(self.request.path)  # Перенаправление на ту же страницу
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProfileView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context
