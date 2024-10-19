from django.views.generic import TemplateView

from OneC.functions import get_exchange_rate
from web_project import TemplateLayout


class CheckView(TemplateView):
    template_name = "OneC/check_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exchange_rate'] = get_exchange_rate()
        return context


class CheckListView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context
