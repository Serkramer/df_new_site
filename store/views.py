from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from dal import autocomplete
from .models import Materials
from django.db.models import Q


class MaterialsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Убедитесь, что пользователь аутентифицирован
        if not self.request.user.is_authenticated and self.request.user.is_staff:
            return Materials.objects.none()

        qs = Materials.objects.all().order_by('name')

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

