import json
from datetime import datetime
from time import sleep
from pathlib import Path
from typing import Union, List
from collections import namedtuple

import pandas as pd

from indicators.schemas import EntrySchema, IndicatorSchema
from indicators.services.common import make_wedriver, make_request_client
from indicators.countries import USA as COUNTRY

_COMPOSITE_LEADING_INDICATOR = IndicatorSchema(
    country=COUNTRY,
    name="Composite leading indicator",
    code="CLI",
    url="https://data.oecd.org/leadind/composite-leading-indicator-cli.htm#indicator-chart",
)

_BUSINESS_CONFIDENCE_INDEX = IndicatorSchema(
    country=COUNTRY,
    name="Business confidence index",
    code="BCI",
    url="https://data.oecd.org/leadind/business-confidence-index-bci.htm#indicator-chart",
)

_CONSUMER_CONFIDENCE_INDEX = IndicatorSchema(
    country=COUNTRY,
    name="Consumer confidence index",
    code="CCI",
    url="https://data.oecd.org/leadind/consumer-confidence-index-cci.htm#indicator-chart",
)

INDICATORS: List[IndicatorSchema] = [
    _COMPOSITE_LEADING_INDICATOR,
    _BUSINESS_CONFIDENCE_INDEX,
    _CONSUMER_CONFIDENCE_INDEX,
]


def _get_csv_link(url: str) -> str:
    driver = make_wedriver()
    driver.get(url)

    sleep(5)

    driver.execute_script(
        """
            document.querySelector("[class='chart-button-panel']")
                    .getElementsByTagName("li")[2]
                    .querySelector("[class*='download-btn']")
                    .click();
        """
    )

    driver.execute_script(
        """
            document.querySelector("[class='chart-button-panel']")
                    .getElementsByTagName("li")[2]
                    .querySelector("[class='download-indicator-button']")
                    .click();
        """
    )

    link = driver.execute_script(
        """
            return document.querySelector("[class='chart-button-panel']")
                            .getElementsByTagName("li")[2]
                            .querySelector("[class='download-indicator-button']")
                            .getAttribute("href");
        """
    )

    driver.quit()
    return link


CSVData = namedtuple("CSVData", ["path", "indicator"])


def _download_csv(indicator: IndicatorSchema) -> CSVData:
    link = _get_csv_link(indicator.url)  # type: ignore
    client = make_request_client()
    response = client.get(link)

    name = str(datetime.now()).replace(" ", "_").replace(":", "_").replace(".", "_")
    Path("downloaded").mkdir(exist_ok=True)
    path = Path(f"downloaded/{name}.csv")

    with open(path, "w", encoding="utf-8") as file:
        file.write(response.text)

    return CSVData(path=path, indicator=indicator)


def _extract_output_data(csv_data: List[CSVData]) -> List[EntrySchema]:
    entries: List[EntrySchema] = []

    for csv_item in csv_data:
        indicator = csv_item.indicator
        df = pd.read_csv(csv_item.path)
        json_data = json.loads(df.to_json(orient="records"))

        for item in json_data:
            if item["LOCATION"] != COUNTRY.code:
                continue

            prev_value: Union[float, None] = None
            current_value: Union[float, None] = None

            try:
                current_value = float(item["Value"])
            except Exception:
                current_value = None

            if current_value is not None and prev_value not in [None, 0.0]:
                perc_change = round(
                    (current_value - prev_value) / prev_value,  # type: ignore
                    ndigits=6
                )
            else:
                perc_change = 0.0

            date = datetime.strptime(item["TIME"], "%Y-%m").date()
            entries.append(
                EntrySchema(
                    country=COUNTRY,
                    name=indicator.name,
                    code=indicator.code,
                    date=date,
                    value1=current_value,
                    perc_change1=perc_change,
                )
            )

            prev_value = current_value

    return entries


def get_entries() -> List[EntrySchema]:
    output_data: List[EntrySchema] = _extract_output_data(
        [_download_csv(item) for item in INDICATORS]
    )
    return output_data
