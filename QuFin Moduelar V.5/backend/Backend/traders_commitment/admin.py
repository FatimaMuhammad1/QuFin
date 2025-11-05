from django.contrib import admin

from .models import Currency, CoTFin, CurrencyValue


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "verbose_name"]


class CurrencyValueAdmin(admin.ModelAdmin):
    list_display = ["id", "currency", "timestamp", "open_price",
                    "close_price", "high_price", "low_price",
                    "adj_close_price"]


class CoTFinAdmin(admin.ModelAdmin):
    list_display = ["id", "currency", "date"]


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyValue, CurrencyValueAdmin)
admin.site.register(CoTFin, CoTFinAdmin)
