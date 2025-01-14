from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

from django.shortcuts import render
from dal import autocomplete
from django.views import View
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


class CompaniesTableView(TemplateView):
    template_name = 'custom/company_tables.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['title'] = 'Компанії'
        return context


class CompaniesTableDataView(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', Companies.objects.all().count()))
        search_value = request.GET.get('search[value]', '').strip()
        companies_queryset = Companies.objects.all().order_by('name')

        if search_value:
            companies_queryset = companies_queryset.filter(
                Q(name__icontains=search_value),
                Q(full_name__icontains=search_value),
                Q(number__icontains=search_value),
                Q(okpo__icontains=search_value)
            )

        records_total = Companies.objects.count()
        records_filtered = companies_queryset.count()
        companies = companies_queryset[start:start + length]

        data = [
            {
                'id': company.id,
                'full_name': company.full_name if company.full_name else '-',
                'name': company.name if company.name else '-',
                'okpo': company.okpo if company.okpo else '-',
                'is_verified': company.is_verified,
                'is_outdated': company.is_outdated,
                'number': company.number if company.number else '-',
                'delivery': company.delivery_preset.__str__() if company.delivery_preset else '-',
                'group': company.company_group.name if company.company_group else '-',


            } for company in companies
        ]

        response = {'data': data,
                    'draw': draw,
                    'recordsTotal': records_total,
                    'recordsFiltered': records_filtered,
                    }

        return JsonResponse(response)


class CompaniesCardView(TemplateView):
    template_name = 'custom/companies_card.html'
    form_class = CompaniesCardViewForm

    def get_context_data(self, **kwargs):
        """
        Добавляем контекст для отображения в шаблоне.
        """
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        company_id = self.kwargs.get('id')
        company = get_object_or_404(Companies, id=company_id) if company_id else None

        # Основная форма
        form = self.form_class(instance=company)

        # Формсеты
        clients_formset = self.form_class.CompanyClientsFormSet(instance=company)
        printing_company_formset = self.form_class.PrintingCompaniesFormSet(instance=company)
        company_contacts_formset = self.form_class.CompaniesContactsFormSet(instance=company)
        delivery_preset_formset = self.form_class.DeliveryPresetsFormSet(instance=company)

        context.update({
            'company': company,
            'form': form,
            'clients_formset': clients_formset,
            'printing_company_formset': printing_company_formset,
            'company_contacts_formset': company_contacts_formset,
            'delivery_preset_formset': delivery_preset_formset,
            'title': 'Редагувати компанію' if company_id else 'Додати компанію',
        })
        return context

    def post(self, request, *args, **kwargs):
        """
        Обрабатываем POST-запрос: валидация и сохранение данных.
        """
        action = request.POST.get('action')
        company_id = self.kwargs.get('id')
        company = get_object_or_404(Companies, id=company_id) if company_id else None

        # Основная форма
        form = self.form_class(request.POST, instance=company)

        # Формсеты
        clients_formset = self.form_class.CompanyClientsFormSet(request.POST, instance=company)
        printing_company_formset = self.form_class.PrintingCompaniesFormSet(request.POST, instance=company)
        company_contacts_formset = self.form_class.CompaniesContactsFormSet(request.POST, instance=company)
        delivery_preset_formset = self.form_class.DeliveryPresetsFormSet(request.POST, instance=company)

        # Обработка действий
        if action == 'save_company':
            if form.is_valid():
                form.save()
                return redirect('custom:edit_company_card', id=form.instance.id)
            else:
                print("Форма компании не прошла валидацию")
                print(form.errors)

        elif action == 'save_client':

            # Получаем экземпляры формы без сохранения в базе данных

            instances = clients_formset.save(commit=False)
            # Переприсваиваем объект компании всем экземплярам

            for instance in instances:
                instance.company = company  # Связываем объект CompanyClients с объектом компании
            # Выполняем валидацию на этом этапе
            if clients_formset.is_valid():
                # Сохраняем все экземпляры
                for instance in instances:
                    instance.save()  # Сохраняем каждый экземпляр в базе данных

                clients_formset.save_m2m()  # Сохраняем многие ко многим связи

                return redirect('custom:edit_company_card', id=company.id)

            else:

                print("Клиенты: ошибки в формсете")
                print(clients_formset.errors)

        elif action == 'save_printing_company':
            if printing_company_formset.is_valid():
                printing_company_formset.save()
                return redirect('custom:edit_company_card', id=company.id)
            else:
                print("Печать: ошибки в формсете")
                print(printing_company_formset.errors)

        elif action == 'save_company_contacts':
            if company_contacts_formset.is_valid():
                company_contacts_formset.save()
                return redirect('custom:edit_company_card', id=company.id)
            else:
                print("Контакты: ошибки в формсете")
                print(company_contacts_formset.errors)

        elif action == 'save_delivery_presets':
            if delivery_preset_formset.is_valid():
                delivery_preset_formset.save()
                return redirect('custom:edit_company_card', id=company.id)
            else:
                print("Доставка: ошибки в формсете")
                print(delivery_preset_formset.errors)

        # Если форма или формсет не прошли валидацию, передаем их обратно в шаблон
        context = self.get_context_data(**kwargs)
        context.update({
            'company': company,
            'form': form,
            'clients_formset': clients_formset,
            'printing_company_formset': printing_company_formset,
            'company_contacts_formset': company_contacts_formset,
            'delivery_preset_formset': delivery_preset_formset,
        })
        return self.render_to_response(context)
