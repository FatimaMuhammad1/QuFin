import json
import calendar
from datetime import datetime
from typing import Union, List

from indicators.countries import USA
from indicators.schemas import EntrySchema, IndicatorSchema

from .indicators import INDICATORS


def get_indicators() -> List[IndicatorSchema]:
    return INDICATORS


def extract_data_from_files(indicators: List[IndicatorSchema]) -> List[EntrySchema]:
    entries: List[EntrySchema] = []

    for indicator in indicators:
        if indicator.file is not None:
            with open(indicator.file, "r", encoding="utf-8") as file:
                print(indicator.file)
                data = json.load(file)["data"]
                series = list(data.values())[0]["s"][0]

                prev_value: Union[float, None] = None
                current_value: Union[float, None] = None

                for item in series:
                    date_str, value_str = item

                    try:
                        current_value = float(value_str)
                    except Exception:
                        current_value = None

                    if current_value is not None and prev_value not in [None, 0.0]:
                        perc_change = round(
                            (current_value - prev_value) / prev_value, # type: ignore
                            ndigits=6
                        )
                    else:
                        perc_change = 0.0
                    
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    entry = EntrySchema(
                        country=USA,
                        name=indicator.name,
                        code=indicator.code,
                        date=date,
                        value1=current_value,
                        perc_change1=perc_change
                    )
                    entries.append(entry)

                    prev_value = current_value

    return entries


def get_passed_month_name() -> str:
    now = datetime.now()
    return calendar.month_name[now.month].lower()


def get_entries() -> List[EntrySchema]:
    output_data: List[EntrySchema] = []
    output_data.extend(extract_data_from_files(
        indicators=get_indicators()
    ))
    return output_data
