from typing import List

from django.db import transaction

from indicators.schemas import EntrySchema, CountrySchema
from indicators.models import Entry, Country, Indicator


def populate_db(entries_data: List[EntrySchema]):
    with transaction.atomic():
        try:
            for entry_data in entries_data:
                country = _get_country(entry_data.country)
                indicator = _get_indicator(entry_data, country)
                _get_or_update_entry(entry_data, indicator)
        except Exception as e:
            transaction.rollback()
            print(e)


def _get_country(data: CountrySchema) -> Country:
    try:
        country = Country.objects.get(code=data.code)
    except Country.DoesNotExist:
        country = Country.objects.create(
            name=data.name,
            code=data.code
        )
    return country


def _get_indicator(data: EntrySchema, country: Country) -> Indicator:
    try:
        indicator = Indicator.objects.get(
            country__code=country.code,
            name=data.name,
            code=data.code
        )
    except Indicator.DoesNotExist:
        indicator = Indicator.objects.create(
            country=country,
            name=data.name,
            code=data.code,
            frequency=str(data.frequency.value),
            unit=data.unit
        )
    return indicator


def _get_or_update_entry(data: EntrySchema, indicator: Indicator) -> Entry:
    try:
        entry = Entry.objects.get(
            indicator__code=indicator.code,
            indicator__country=indicator.country,
            date=data.date
        )
    except Entry.DoesNotExist:
        entry = Entry.objects.create(
            indicator=indicator,
            date=data.date,
            unit=data.unit,
            value1=data.value1,
            value2=data.value2,
            value3=data.value3,
            perc_change1=data.perc_change1,
            perc_change2=data.perc_change2,
            perc_change3=data.perc_change3,
            value1_name=data.value1_name,
            value2_name=data.value2_name,
            value3_name=data.value3_name,
        )
    return entry
