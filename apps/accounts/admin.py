from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from .forms import CustomAdminUserChangeForm, CustomAdminUserCreationForm
from .models import Timezone, User

admin.site.site_header = mark_safe(
    '<strong style="font-weight:bold;">B.A. V1 ADMIN</strong>'
)


class Group(DjangoGroup):
    class Meta:
        verbose_name = "group"
        verbose_name_plural = "groups"
        proxy = True


class GroupAdmin(BaseGroupAdmin):
    pass


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    add_form = CustomAdminUserCreationForm
    form = CustomAdminUserChangeForm
    model = User

    list_display = [
        "pkid",
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]

    list_display_links = ["id", "email"]
    list_filter = [
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]
    fieldsets = (
        (
            _("Login Credentials"),
            {"fields": ("email", "password")},
        ),
        (
            _("Personal Information"),
            {"fields": ("first_name", "last_name", "tz", "avatar")},
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_email_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important Dates"),
            {"fields": ("date_joined", "last_login")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "tz",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    search_fields = ["email", "first_name", "last_name"]

    def render_change_form(
        self, request, context, obj, add=False, change=False, form_url=""
    ):
        if not "/add/" in request.path:
            # Allow only super users and article owner to update article
            if request.user != obj and request.user.is_superuser != True:
                context.update(
                    {
                        "show_save": False,
                        "show_save_and_continue": False,
                        "show_delete": False,
                        "show_save_and_add_another": False,
                    }
                )
        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            self.readonly_fields = [
                "groups",
                "user_permissions",
                "is_staff",
                "is_superuser",
                "is_active",
            ]
        return self.readonly_fields


class TimezoneAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    list_filter = ["name", "created_at"]


admin.site.register(User, UserAdmin)
admin.site.register(Timezone, TimezoneAdmin)

admin.site.register(Group, GroupAdmin)
admin.site.unregister(DjangoGroup)
