from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

from django.shortcuts import render
from dal import autocomplete
from django.views.generic import TemplateView, FormView

from web_project import TemplateLayout
from .forms import CompaniesCardViewForm
from .models import CompanyClients, PrintingCompanies, PrintingMachinePresets, ClicheTechnologies, CompaniesContacts, \
    Contacts, Companies
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


class PrintingCompaniesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated and self.request.user.is_staff:
            return PrintingCompanies.objects.none()

        qs = PrintingCompanies.objects.select_related('id').all().order_by('id__name')

        company_client = self.forwarded.get('company_client')
        if company_client:
            # Фильтруем печатные компании, связанные с этим клиентом через ClientUsePrintingCompany
            qs = qs.filter(clientuseprintingcompany__company_client=company_client)

        if self.q:
            qs = qs.filter(id__name__icontains=self.q)

        return qs


class PrintingMachinePresetsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated and self.request.user.is_staff:
            return PrintingMachinePresets.objects.none()

        qs = PrintingMachinePresets.objects.select_related('printing_machine__printing_company').all()

        # Получаем печатную компанию из forwarded данных
        printing_company = self.forwarded.get('printing_company')

        if printing_company:
            # Фильтруем пресеты, связанные с машинами данной печатной компании
            qs = qs.filter(printing_machine__printing_company_id=printing_company)

        # Фильтр по запросу (по имени пресета)
        if self.q:
            qs = qs.filter(name__icontains=self.q)

        # Сортируем по названию компании и затем по имени пресета
        qs = qs.order_by('printing_machine__printing_company__name', 'name')
        return qs


class ClicheTechnologiesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated and self.request.user.is_staff:
            return PrintingMachinePresets.objects.none()

        qs = ClicheTechnologies.objects.all()

        printing_company = self.forwarded.get('printing_company')
        preset = self.forwarded.get('preset')

        if preset:
            pass
        elif printing_company:
            pass

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class ContactAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Ensure the user is authenticated
        if not self.request.user.is_authenticated:
            return Contacts.objects.none()

        qs = Contacts.objects.all()

        # Filter by the selected company (via CompaniesContacts)
        company_id = self.forwarded.get('company', None)
        if company_id:
            # Filter Contacts related to the given company through CompaniesContacts
            qs = qs.filter(companiescontacts__company_id=company_id)

        # Filter by text search (contact name or description)
        if self.q:
            qs = qs.filter(
                Q(first_name__icontains=self.q) |
                Q(last_name__icontains=self.q) |
                Q(middle_name__icontains=self.q) |
                Q(description__icontains=self.q)
            )

        return qs


class CompaniesCardView(FormView):
    template_name = 'custom/companies_card.html'
    form_class = CompaniesCardViewForm

    def get_initial(self):
        """
        Устанавливает начальные данные для формы при редактировании.
        """
        initial = super().get_initial()
        company_id = self.kwargs.get('id')  # Получаем id из URL
        if company_id:
            company = get_object_or_404(Companies, id=company_id)
            initial.update({
                'full_name': company.full_name,
                'name': company.name,
                'okpo': company.okpo,
                'delivery_preset': company.delivery_preset,
                'number': company.number,
                # Другие поля, если нужно
            })
        return initial

    def get_form_kwargs(self):
        """
        Передает instance в форму для редактирования объекта.
        """
        kwargs = super().get_form_kwargs()
        company_id = self.kwargs.get('id')
        if company_id:
            kwargs['instance'] = get_object_or_404(Companies, id=company_id)
        return kwargs

    def form_valid(self, form):
        """
        Сохраняем данные формы и formset.
        """
        form.instance = form.save()  # Сохраняем компанию
        clients_formset = form.clients_formset
        printing_company_formset = form.printing_company_formset
        company_contacts_formset = form.company_contacts_formset
        if company_contacts_formset.is_valid():
            company_contacts_formset.save()
        if printing_company_formset.is_valid():
            printing_company_formset.save()
        if clients_formset.is_valid():
            clients_formset.save()  # Сохраняем данные из formset

        if form.printing_machines_formset:
            if form.printing_machines_formset.is_valid():
                form.printing_machines_formset.save()
        return redirect('company_card')  # Перенаправление после сохранения

    def get_context_data(self, **kwargs):
        """
        Добавляем контекст для шаблона.
        """
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        company_id = self.kwargs.get('id')
        context['title'] = 'Редагувати компанію' if company_id else 'Додати компанію'
        return context

