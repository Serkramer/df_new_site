
from django.views.generic import TemplateView

from custom.models import PrintingMachineShafts
from web_project import TemplateLayout


# Create your views here.


class PrintingRollersView(TemplateView):
    template_name = "info/printings_rollers.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        shafts = PrintingMachineShafts.objects.all()
        context['shafts'] = shafts
        return context

