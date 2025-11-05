from core.models import TimeStampedModel
from django.db import models


class Currency(TimeStampedModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} ({self.name})"


class ExchangeRate(TimeStampedModel):
    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="base_currency")
    quote_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="quote_currency")
    value = models.DecimalField(max_digits=20, decimal_places=10)

    class Meta:
        unique_together = ("base_currency", "quote_currency", "created_at")

    def __str__(self):
        return f"{self.base_currency}-{self.quote_currency}: {self.value}"
