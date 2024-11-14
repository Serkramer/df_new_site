from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Profile


# Register your models here.
class Member(admin.ModelAdmin):
    list_display = (
        "user",
        "email",
        "is_verified",
        "created_at",
    )


# admin.site.register(Profile, Member)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'company', 'phone_number', 'email',
                    'is_verified', 'created_at', 'post_avatar')

    @admin.display(description="Аватарка", ordering='content')
    def post_avatar(self, obj):
        if obj.avatar:
            return mark_safe(f"<img src='{obj.avatar.url}' width=50>")
        return "-"
