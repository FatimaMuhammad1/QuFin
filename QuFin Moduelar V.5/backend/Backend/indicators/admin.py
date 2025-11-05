from django.contrib import admin
from django.conf import settings

from .models import Country, Indicator, Entry


class ObjectPermissionMixin:
    def has_add_permission(self, request) -> bool:
        return False
    
    def has_delete_permission(self, request, obj=None) -> bool:
        return settings.DEBUG


class CountryAdmin(admin.ModelAdmin, ObjectPermissionMixin):
    list_display = ["id", "name", "code"]


class IndicatorAdmin(admin.ModelAdmin, ObjectPermissionMixin):
    list_display = ["id", "name", "code", "country", "frequency"]
    list_filter = ["country", "frequency"]


class EntryAdmin(admin.ModelAdmin, ObjectPermissionMixin):
    list_display = ["id", "indicator", "date", "get_value1", "get_value2", "get_value3"]
    list_filter = ["indicator"]

    def get_value1(self, obj=None):
        if obj is None:
            return "-"
        return f"{obj.value1} ({obj.perc_change1}%)"
    get_value1.short_description = "Main value"

    def get_value2(self, obj=None):
        if obj is None:
            return "-"
        return f"{obj.value2} ({obj.perc_change2}%)"
    get_value2.short_description = "Extra value"

    def get_value3(self, obj=None):
        if obj is None:
            return "-"
        return f"{obj.value3} ({obj.perc_change3}%)"
    get_value3.short_description = "Extra value 2"


admin.site.register(Country, CountryAdmin)
admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(Entry, EntryAdmin)