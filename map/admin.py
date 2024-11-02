from django.contrib import admin

from map.models import Settlements, Areas, PostOffices


# Register your models here.

@admin.register(Settlements)
class SettlementsAdmin(admin.ModelAdmin):
    list_display = ('description', )
    search_fields = ('description', )


@admin.register(Areas)
class AreasAdmin(admin.ModelAdmin):
    list_display = ('description', 'ref')
    search_fields = ('description',)


@admin.register(PostOffices)
class PostOfficesAdmin(admin.ModelAdmin):
    list_display = ('description', 'number', 'phone', 'place_max_weight_allowed', 'short_address', 'settlement')
    search_fields = ('description', 'number')
