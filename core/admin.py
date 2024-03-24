from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User

    # fieldsets = (
    #     (
    #         None,
    #         {
    #             "fields": (
    #                 "email",
    #                 "first_name",
    #                 "last_name",
    #                 "phone_number",
    #                 "password",
    #             )
    #         },
    #     ),
    #     ("Permissions", {"fields": ("is_staff", "is_active")}),
    # )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    list_display = [
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "id",
        "is_active",
        "is_superuser",
        "is_staff",
    ]
    search_fields = ["email", "first_name", "last_name"]
    ordering = [
        "email",
    ]


admin.site.register(get_user_model(), CustomUserAdmin)
