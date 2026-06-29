from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Payment, User


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    list_display = ["email", "phone", "city", "is_staff"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Личная информация", {"fields": ("phone", "city", "avatar")}),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = ((None, {"fields": ("email", "password1", "password2")}),)
    search_fields = ["email"]


admin.site.register(User, UserAdmin)
admin.site.register(Payment)
