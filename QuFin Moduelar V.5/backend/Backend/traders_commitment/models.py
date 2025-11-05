from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=50)
    verbose_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self) -> str:
        return f"{self.name}"


class CurrencyValue(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                 related_name="values")
    timestamp = models.DateField()
    open_price = models.FloatField(null=True, blank=True)
    close_price = models.FloatField(null=True, blank=True)
    high_price = models.FloatField(null=True, blank=True)
    low_price = models.FloatField(null=True, blank=True)
    adj_close_price = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Currency value"
        verbose_name_plural = "Currency values"

    def __str__(self) -> str:
        return str(self.currency)


class CoTFin(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                 related_name="cotfins")
    date = models.DateField()

    asset_manager_positions_long = models.IntegerField(null=True, blank=True)
    asset_manager_positions_short = models.IntegerField(null=True, blank=True)
    asset_manager_positions_long_short = models.IntegerField(null=True, blank=True)

    leverage_money_positions_long = models.IntegerField(null=True, blank=True)
    leverage_money_positions_short = models.IntegerField(null=True, blank=True)
    leverage_money_positions_long_short = models.IntegerField(null=True, blank=True)

    other_rept_positions_long_all = models.IntegerField(null=True, blank=True)
    other_rept_positions_short_all = models.IntegerField(null=True, blank=True)
    other_rept_positions_long_short_all = models.IntegerField(null=True, blank=True)

    percentage_of_open_interest_asset_manager_long = models.IntegerField(null=True, blank=True)
    percentage_of_open_interest_asset_manager_short = models.IntegerField(null=True, blank=True)
    percentage_of_open_interest_asset_manager_long_short = models.IntegerField(null=True, blank=True)

    percentage_of_leverage_money_asset_manager_long = models.IntegerField(null=True, blank=True)
    percentage_of_leverage_money_asset_manager_short = models.IntegerField(null=True, blank=True)
    percentage_of_leverage_money_asset_manager_long_short = models.IntegerField(null=True, blank=True)

    percentage_of_other_rept_positions_long_all = models.IntegerField(null=True, blank=True)
    percentage_of_other_rept_positions_short_all = models.IntegerField(null=True, blank=True)
    percentage_of_other_rept_positions_long_short_all = models.IntegerField(null=True, blank=True)


    def __str__(self) -> str:
        return str(self.currency)

    class Meta:
        verbose_name = "COT (Financial Reports only) data"
        verbose_name_plural = "COT (Financial Reports only) data"


class CoTFORScrapedStatus(models.Model):
    url = models.TextField(unique=True)
    file = models.FileField(upload_to="cotfor/")
    date = models.DateField()
    is_parsed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "{}: {}".format(str(self.created_at), str(self.file))
