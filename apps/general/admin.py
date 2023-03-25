from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from import_export import resources
from import_export.admin import ExportActionMixin
from .models import *


class SiteDetailAdmin(admin.ModelAdmin):
    fieldsets = (
        ("General", {"fields": ["name", "email", "phone", "address"]}),
        ("Social", {"fields": ["fb", "tw", "wh", "ig"]}),
    )

    def has_add_permission(self, request):
        return (
            False
            if self.model.objects.count() > 0
            else super().has_add_permission(request)
        )

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.all()[0]
        return HttpResponseRedirect(
            reverse(
                "admin:%s_%s_change"
                % (self.model._meta.app_label, self.model._meta.model_name),
                args=(obj.pkid,),
            )
        )


class SuscriberResource(resources.ModelResource):
    class Meta:
        model = Suscriber
        fields = ("email",)

    def after_export(self, queryset, data, *args, **kwargs):
        queryset.update(exported=True)
        return queryset


class SuscriberAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["email", "exported"]
    list_filter = ["email", "exported"]
    resource_class = SuscriberResource


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "name", "show"]
    list_filter = ["user", "name", "show"]


admin.site.register(SiteDetail, SiteDetailAdmin)
admin.site.register(Suscriber, SuscriberAdmin)
admin.site.register(Review, ReviewAdmin)
