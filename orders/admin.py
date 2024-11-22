
from django.contrib import admin
from django.utils.safestring import mark_safe
from orders.models import FilesAllowedExtensions, RegistrationSamples, DesignRegister
from django.utils.html import format_html

# Register your models here.


@admin.register(FilesAllowedExtensions)
class FilesAllowedExtensionsAdmin(admin.ModelAdmin):
    list_display = ('extension', 'work_file')


@admin.register(RegistrationSamples)
class RegistrationSampleAdmin(admin.ModelAdmin):
    list_display = ('name', 'our_manager', 'contact', 'post_img')

    def post_img(self, obj: RegistrationSamples):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50">')
        return "Без зображення"

    post_img.short_description = "Фото"


@admin.register(DesignRegister)
class DesignRegister(admin.ModelAdmin):
    list_display = ('date_created', 'view_id', 'name', 'company_client_display', 'manager', 'designer', 'status')

    def view_id(self, obj):
        if obj.pk:
            return f"D{obj.pk}"
        else:
            return "-"

    view_id.short_description = "ID макета"

    view_id.short_description = "D"

    def company_client_display(self, obj):
        # Здесь происходит попытка найти объект CompanyClients по ID
        try:
            from custom.models import CompanyClients  # Импорт модели
            client = CompanyClients.objects.get(pk=obj.company_client_id)
            return client.id.name
        except CompanyClients.DoesNotExist:
            return "Не найдено"

    company_client_display.short_description = "Клиент"


