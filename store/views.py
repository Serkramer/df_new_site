from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from dal import autocomplete
from .models import Materials
from django.db.models import Q


class MaterialsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Убедитесь, что пользователь аутентифицирован
        if not self.request.user.is_authenticated:
            return Materials.objects.none()

        qs = Materials.objects.all().order_by('name')

        thickness_list = self.forwarded.get('thickness')
        if thickness_list:
            qs = qs.filter(thickness__in=thickness_list)

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
