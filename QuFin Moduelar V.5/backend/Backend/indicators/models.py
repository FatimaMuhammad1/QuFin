from django.db import models

# Standard Django choices tuple
FREQUENCY_CHOICES = (
    (1, "Daily"),
    (2, "Weekly"),
    (3, "Monthly"),
    (4, "Quarterly"),
    (5, "Annually"),
)


class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=6, unique=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self) -> str:
        return f"{self.name}"


class Indicator(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default=3,  # Default to "Monthly"
    )
    unit = models.CharField(max_length=125, null=True, blank=True)

    class Meta:
        verbose_name = "Indicator"
        verbose_name_plural = "Indicators"

    def __str__(self) -> str:
        return "{} ({})".format(self.name, self.country.code)


class Entry(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    date = models.DateField()
    unit = models.CharField(max_length=125, null=True, blank=True)
    value1_name = models.CharField(max_length=255, null=True, blank=True)
    value1 = models.FloatField(max_length=30, null=True)
    value2_name = models.CharField(max_length=255, null=True, blank=True)
    value2 = models.FloatField(max_length=30, null=True, blank=True)
    value3_name = models.CharField(max_length=255, null=True, blank=True)
    value3 = models.FloatField(max_length=30, null=True, blank=True)
    total_value = models.FloatField(max_length=30, null=True, blank=True)
    perc_change1 = models.FloatField(default=0.0, verbose_name="Percentage of Change")
    perc_change2 = models.FloatField(
        null=True, blank=True, verbose_name="Percentage of Change (extra)"
    )
    perc_change3 = models.FloatField(
        null=True, blank=True, verbose_name="Percentage of Change (extra)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Entry"
        verbose_name_plural = "Entries"

    def __str__(self) -> str:
        return str(self.indicator)
