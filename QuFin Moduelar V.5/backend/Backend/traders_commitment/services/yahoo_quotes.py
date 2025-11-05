import logging
import json
import os
from datetime import datetime

import httpx
from django.conf import settings
from django.db import transaction

from traders_commitment.models import Currency, CurrencyValue
from traders_commitment.schemas import CurrencyData, CurrencyValueData


from traders_commitment.constants import YAHOO_QUOTE_RANGE, CURRENCIES


logger = logging.getLogger(__name__)


def __download_yahoo_currency_data(code: str, range: YAHOO_QUOTE_RANGE) -> dict:
    url_template = "https://query1.finance.yahoo.com/v8/finance/chart/{}"

    params = {
        "region": "US",
        "lang": "en-US",
        "includePrePost": "false",
        "interval": "1mo",
        "useYfid": "true",
        "range": range,
        "corsDomain": "finance.yahoo.com",
        ".tsrc": "finance"
    }

    headers = {
        "accept": "*/*",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "Referer": "https://finance.yahoo.com/",
        "Referrer-Policy": "no-referrer-when-downgrade"
    }

    url = url_template.format(code)

    logger.info(f"Getting data from yahoo for {code} at {url}")

    response = httpx.get(url, params=params, headers=headers)

    if settings.DEBUG:
        logger.info("DEBUG=True | saving the data in the temp_data folder")

        filename = f"{str(datetime.now())}.json"
        removables = [":", "-", " "]
        for item in removables:
            filename = filename.replace(item, "_")

        path = os.path.join("media", "data", filename)
        with open(path, "w") as file:
            json.dump(response.json(), file)
        
        logger.info(f"File saved at {str(path)}")

    return response.json()


def __parse_yahoo_currency_data(
        currency: CurrencyData,
        data: dict
    ) -> list[CurrencyValueData]:
    timestamps = data['chart']['result'][0]['timestamp']
    indicators = data['chart']['result'][0]['indicators']
    quote_data = indicators['quote'][0]
    open_prices = quote_data['open']
    close_prices = quote_data['close']
    high_prices = quote_data['high']
    low_prices = quote_data['low']
    adj_close_prices = indicators['adjclose'][0]['adjclose']

    logger.info(f"Starting to parse yahoo data for {currency.name}")

    output: list[CurrencyValueData] = []
    for i in range(len(timestamps)):
        currency_value = CurrencyValueData(
            currency=currency,
            timestamp=datetime.fromtimestamp(timestamps[i]).date(),
            open_price=open_prices[i],
            close_price=close_prices[i],
            low_price=low_prices[i],
            high_price=high_prices[i],
            adj_close_price=adj_close_prices[i]
        )
        output.append(currency_value)
    
    logger.info(f"Finished parsing yahoo data for {currency.name} | {len(output)} items")

    return output


def populate_db_with_yahoo_quotes(data: list[CurrencyValueData]):
    fields_mapping = [
        "timestamp",
        "open_price",
        "close_price",
        "high_price",
        "low_price",
        "adj_close_price",
    ]

    currenies: dict[str, Currency] = {}

    logger.info(f"Starting to populate the db with yahoo data | {len(data)} items")

    with transaction.atomic():
        try:
            for item in data:
                currency_kwargs = {
                    "name": item.currency.name,
                    "verbose_name": item.currency.verbose_name
                }
                if item.currency.name in currenies:
                    currency = currenies[item.currency.name]
                else:
                    currency = Currency.objects.filter(**currency_kwargs).first()
                    if currency is None:
                        currency, _ = Currency.objects.get_or_create(**currency_kwargs)
                    currenies[item.currency.name] = currency

                kwargs = {"currency": currency}
                for field in fields_mapping:
                    kwargs[field] = getattr(item, field)
                
                CurrencyValue.objects.get_or_create(**kwargs)
        except Exception as e:
            transaction.rollback()
            logger.info("Couldn't populate the db")
            logger.info(f"Error: {str(e)}")
        finally:
            logger.info(f"Finished populating the db | {len(data)} items")


def parse_yahoo_quotes(range: YAHOO_QUOTE_RANGE = "max") -> list[CurrencyValueData]:
    output: list[CurrencyValueData] = []

    for item in CURRENCIES:
        data: list[CurrencyValueData] = __parse_yahoo_currency_data(
            currency=item,
            data=__download_yahoo_currency_data(
                code=item.name,
                range=range
            )
        )
        output.extend(data)
    
    return output
