from django.views.generic import TemplateView

from OneC.functions import get_exchange_rate


class CheckView(TemplateView):
    template_name = "OneC/check_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exchange_rate'] = get_exchange_rate()
        return context

