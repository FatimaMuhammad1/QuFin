import io
import csv
import asyncio
from datetime import datetime
from typing import Union, List, Dict

import httpx
from indicators.schemas import EntrySchema, IndicatorSchema
from indicators.countries import AUS

from .indicators import INDICATORS

_BASE_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"


def get_indicators() -> List[IndicatorSchema]:
    return INDICATORS


async def _async_get_all_data(
    indicators: List[IndicatorSchema],
    start_date: str = "1950-01-01",
    end_date: str = str(datetime.now().date()),
) -> Dict[IndicatorSchema, httpx.Response]:
    results: List[httpx.Response] = []

    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = [
            client.get(
                _BASE_URL,
                params={"id": indicator.code, "cosd": start_date, "coed": end_date},
            )
            for indicator in indicators
        ]
        results = await asyncio.gather(*tasks)

    responses: Dict[IndicatorSchema, httpx.Response] = dict()

    for indicator, result in zip(indicators, results):
        responses[indicator] = result

    return responses


def _collect_responses(
    indicators: List[IndicatorSchema],
) -> Dict[IndicatorSchema, httpx.Response]:
    loop = asyncio.get_event_loop()
    results: Dict[IndicatorSchema, httpx.Response] = loop.run_until_complete(
        _async_get_all_data(indicators=indicators)
    )
    return results


def _extract_output_data(
    responses: Dict[IndicatorSchema, httpx.Response]
) -> List[EntrySchema]:
    entries: List[EntrySchema] = []

    for indicator, response in responses.items():
        prev_value: Union[float, None] = None
        current_value: Union[float, None] = None

        for item in list(csv.DictReader(io.StringIO(response.text))):
            try:
                current_value = float(item[indicator.code])
            except Exception:
                current_value = None

            if current_value is not None and prev_value not in [None, 0.0]:
                perc_change = round(
                    (current_value - prev_value) / prev_value, ndigits=6  # type: ignore
                )
            else:
                perc_change = 0.0

            try:
                item["DATE"]
            except:
                print(item)
                print(indicator.url)
                print("------------------")

            entry = EntrySchema(
                country=AUS,
                name=indicator.name,
                code=indicator.code,
                date=datetime.strptime(item["DATE"], "%Y-%m-%d").date(),
                value1=current_value,
                perc_change1=perc_change,
            )
            entries.append(entry)

            prev_value = current_value

    return entries


def get_entries() -> List[EntrySchema]:
    responses: Dict[IndicatorSchema, httpx.Response] = _collect_responses(
        indicators=get_indicators()
    )
    output_data: List[EntrySchema] = _extract_output_data(responses=responses)
    return output_data
