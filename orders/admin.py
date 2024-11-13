
from django.contrib import admin

from custom.models import Orders
from orders.models import FilesAllowedExtensions


# Register your models here.


@admin.register(FilesAllowedExtensions)
class FilesAllowedExtensionsAdmin(admin.ModelAdmin):
    list_display = ('extension', 'work_file')


