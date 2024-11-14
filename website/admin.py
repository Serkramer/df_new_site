from django.contrib import admin

from website.models import Menu, UserGroupMenu


class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'parent', 'order']
    list_filter = ['parent']
    search_fields = ['name', 'url']


admin.site.register(Menu, MenuAdmin)
admin.site.register(UserGroupMenu)
