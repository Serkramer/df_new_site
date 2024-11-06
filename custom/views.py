from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from dal import autocomplete
from .models import CompanyClients
from django.db.models import Q


class CompanyClientsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Убедитесь, что пользователь аутентифицирован
        if not self.request.user.is_authenticated and self.request.user.is_staff:
            return CompanyClients.objects.none()

        qs = CompanyClients.objects.select_related('id').all().order_by('id__name')

        if self.q:
            qs = qs.filter(id__name__icontains=self.q)

        return qs

