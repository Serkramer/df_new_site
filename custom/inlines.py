from django.contrib import admin
from django.core.exceptions import ValidationError

from .forms import ContactsDetailsForm
from .inline_forms import PrintingMachinesInlineForm, ContactsDetailsInlineForm, CompaniesContactsInlineForm
from .models import PrintingMachines, PrintingMachineShafts, PrintingMachinePresets, AniloxRolls, CompanyClients, \
    PrintingCompanies, DeliveryPresets, CompaniesContacts, ContactsDetails, ContactTypeChoices, Contacts
from django.utils.html import format_html
from django.urls import reverse


class PrintingMachineShaftsInline(admin.TabularInline):  # Или используйте admin.StackedInline для более детального представления
    model = PrintingMachineShafts
    extra = 1  # Число пустых форм для добавления новых объектов
    fields = ['quantity', 'width', 'date_create', 'input_value', 'input_value_type', 'contact', 'printing_width', 'description']
    # classes = ['collapse']


class PrintingMachinePresetsInline(admin.TabularInline):
    model = PrintingMachinePresets
    extra = 1
    fields = ('printing_machine', 'name', 'ruling', 'angle_set', 'raster_dot', 'material_thickness',
              'cliche_technology', 'is_revert_printing', 'color_profile', 'plate_curve_strategy',
              'press_curve_strategy', 'damper', 'description', 'adhesive_tape_thickness_multiplier',
              'adhesive_tape_thickness', 'fartuk', 'material')
    # classes = ['collapse']


class AniloxRollsInline(admin.TabularInline):
    model = AniloxRolls
    extra = 1
    fields = ('line_count', 'transfer_volume', 'type', 'description')
    # classes = ['collapse']


class PrintingMachinesInline(admin.TabularInline):
    model = PrintingMachines
    form = PrintingMachinesInlineForm  # Подключаем кастомную форму
    extra = 1
    fields = ['name', 'fartuk', 'section', 'module', 'view_link']
    readonly_fields = ['view_link']
    # classes = ['collapse']

    def view_link(self, obj):
        if obj.id:
            url = reverse('admin:custom_printingmachines_change', args=[obj.id])
            return format_html('<a href="{}" target="_blank">переглянути</a>', url)
        return "Не збережено"

    view_link.short_description = 'Подивитися'


class CompanyClientsInline(admin.StackedInline):  # Можно использовать TabularInline для таблицы
    model = CompanyClients
    fields = ('is_banned', 'debt', 'company_our_brand', 'document_delivery_type', 'is_prepayment')
    extra = 0  # Это количество дополнительных пустых форм для добавления
    verbose_name = "Клієнт"
    verbose_name_plural = "Клієнти"
    # classes = ['collapse']


class PrintingCompaniesInline(admin.StackedInline):
    model = PrintingCompanies
    fields = ('process_id', 'color_library', 'need_printout', 'use_low_base', 'need_label')
    extra = 0
    verbose_name = "Друкарська компанія"
    verbose_name_plural = "Друкарські компанії"
    # classes = ['collapse']


class DeliveryPresetsInline(admin.TabularInline):
    model = DeliveryPresets
    fields = ('delivery_type', 'name', 'address', 'description', 'contact', 'is_legal_address')
    extra = 0
    verbose_name = "Доставка"
    verbose_name_plural = "Доставки"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "contact":
            # Получаем текущую компанию из запроса
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                # Фильтруем контакты, связанные с текущей компанией
                kwargs["queryset"] = Contacts.objects.filter(
                    id__in=CompaniesContacts.objects.filter(company_id=obj_id).values_list('contact_id', flat=True)
                )
            else:
                # Если компания не выбрана, контакты пустые
                kwargs["queryset"] = Contacts.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class CompaniesContactsInline(admin.TabularInline):
    model = CompaniesContacts
    fields = ('contact', 'position', 'is_logistic', 'comment', 'percent_bonus')
    extra = 1
    verbose_name = "Контакт компанії"
    verbose_name_plural = "Контакти компанії"


class ContactsDetailsInline(admin.TabularInline):
    model = ContactsDetails
    form = ContactsDetailsInlineForm
    fields = ('value', 'types')  # Add the 'type' field here
    extra = 0
    verbose_name = "Контактна інформація"
    verbose_name_plural = "Контактна інформація"


class CompaniesContactsForContactInline(admin.TabularInline):
    model = CompaniesContacts
    fields = ('company', 'position', 'is_logistic', 'percent_bonus', 'comment')
    autocomplete_fields = ['company']
    extra = 1
    verbose_name = "З якими компаніями зв'язаний"
    verbose_name_plural = "З якими компаніями зв'язаний"






