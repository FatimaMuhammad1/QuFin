import asyncio
import json
from pprint import pprint

import httpx

from .models import Currency

AVAILABLE_CURRENCIES = ["USD", "EUR", "JPY", "GBP", "CHF", "CAD", "AUD", "NZD"]


async def fetch_exchange_rate(base_currency: str, target_currencies: List[str]) -> dict:
    async with httpx.AsyncClient() as client:
        symbols = ",".join(target_currencies)
        response = await client.get(
            f"https://api.exchangeratesapi.io/latest?base={base_currency}&symbols={symbols}&access_key=OlCVvZLBnLAvSxZBafJaXFbfaFymBMWB",
        )
        response.raise_for_status()
        data = response.json()
        return data


def fetch_exchange_rates(currencies: List[str]):
    futures = asyncio.gather(*[fetch_exchange_rate(currency, currencies) for currency in currencies])

    loop = asyncio.get_event_loop()

    results = loop.run_until_complete(futures)

    pprint(results)
    with open("temp.json", "w") as file:
        file.write(json.dumps(results))


def populate_database_with_currencies():
    for currency in AVAILABLE_CURRENCIES:
        try:
            Currency.objects.get(code=currency)
        except Currency.DoesNotExist:
            Currency.objects.create(code=currency, name=currency)
        except Currency.MultipleObjectsReturned:
            obj = Currency.objects.filter(code=currency).first()
            Currency.objects.filter(code=currency).exclude(id=obj.id).delete()  # type: ignore


def get_available_currencies() -> List[str]:
    return list(Currency.objects.all().values_list("code", flat=True))


def main():
    populate_database_with_currencies()
    fetch_exchange_rates([*get_available_currencies()])


if __name__ == "__main__":
    main()
