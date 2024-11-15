from django.contrib import admin

from map.models import Settlements, Areas, PostOffices


# Register your models here.

@admin.register(Settlements)
class SettlementsAdmin(admin.ModelAdmin):
    list_display = ('description', )
    search_fields = ('description', )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Areas)
class AreasAdmin(admin.ModelAdmin):
    list_display = ('description', 'ref')
    search_fields = ('description',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PostOffices)
class PostOfficesAdmin(admin.ModelAdmin):
    list_display = ('description', 'number', 'phone', 'place_max_weight_allowed', 'short_address', 'settlement')
    search_fields = ('description', 'number')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
