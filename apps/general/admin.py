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
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.get_or_create()
        return HttpResponseRedirect(
            reverse(
                "admin:%s_%s_change"
                % (self.model._meta.app_label, self.model._meta.model_name),
                args=(obj.pkid,),
            )
        )


class SubscriberResource(resources.ModelResource):
    class Meta:
        model = Subscriber
        fields = ("email",)

    def after_export(self, queryset, data, *args, **kwargs):
        queryset.update(exported=True)
        return queryset


class SubscriberAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["email", "exported", "created_at"]
    list_filter = ["email", "exported", "created_at"]
    resource_class = SubscriberResource


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "show"]
    list_filter = ["user", "show"]


admin.site.register(SiteDetail, SiteDetailAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Review, ReviewAdmin)
