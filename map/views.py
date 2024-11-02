from django.shortcuts import render
from dal import autocomplete
from .models import PostOffices, Settlements, Areas
from django.db.models import Q


class PostOfficeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Убедитесь, что пользователь аутентифицирован
        if not self.request.user.is_authenticated:
            return PostOffices.objects.none()

        qs = PostOffices.objects.all().order_by('number')

        settlement_ref = self.forwarded.get('settlement_ref')
        if settlement_ref:
            qs = qs.filter(settlement=settlement_ref)

        if self.q:
            qs = qs.filter(
                Q(description__icontains=self.q) | Q(number__icontains=self.q)
            )

        return qs


class SettlementsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Settlements.objects.none()

        qs = Settlements.objects.all().order_by('description')

        # Получаем `area_ref` из параметров запроса
        area_ref = self.forwarded.get('area', None)
        if area_ref:
            qs = qs.filter(area_ref=area_ref)

        if self.q:
            qs = qs.filter(Q(description__icontains=self.q))

        return qs


class AreasAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Areas.objects.none()

        qs = Areas.objects.all().order_by('description')

        if self.q:
            qs = qs.filter(Q(description__icontains=self.q))

        return qs

