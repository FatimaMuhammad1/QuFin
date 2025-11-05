from datetime import datetime
from typing import List

import httpx

from indicators.schemas import EntrySchema, IndicatorSchema, Frequency
from indicators.countries import USA

from . import get_last_day_of_the_month


__DEBT_TO_PENNY = IndicatorSchema(
    country=USA,
    code="Public Debt (Daily)",
    name="Federal Debt [Debt to Penny (public & intragovernmental)]",
    url="https://fiscaldata.treasury.gov/datasets/debt-to-the-penny/debt-to-the-penny",
    frequency=Frequency.DAILY
)


def __parse_debt_to_penny():
    now = get_last_day_of_the_month()

    url = "https://api.fiscaldata.treasury.gov/services/api/"\
            "fiscal_service/v2/accounting/od/debt_to_penny"

    base_url = "https://api.fiscaldata.treasury.gov/services/api/"\
               "fiscal_service/v2/accounting/od/debt_to_penny"\
              f"?filter=record_date:gte:1993-04-01,record_date:lte:{now.year}-{now.month}-{now.day}"\
               "&sort=-record_date"

    url = base_url + "&page[number]=1&page[size]=10000"

    response = httpx.get(url)
    data = response.json()["data"]

    debts = {}

    while True:
        for item in data:
            debts[item["record_date"]] = float(item["tot_pub_debt_out_amt"])

        links = response.json()["links"]

        if links["next"] is None:
            break

        next_url = base_url + links["next"]
        response = httpx.get(next_url)
        data = response.json()["data"]

    return debts


def get_entries() -> List[EntrySchema]:
    output_data: List[EntrySchema] = []
    data = __parse_debt_to_penny()

    prev_value = None

    dates = list(data.keys())
    dates.sort()

    for key in dates:
        value = data[key]

        if prev_value not in [None, 0.0]:
            perc_change = round(
                (value - prev_value) / prev_value,
                ndigits=6
            )
        else:
            perc_change = 0.0


        output_data.append(EntrySchema(
            country=__DEBT_TO_PENNY.country,
            name=__DEBT_TO_PENNY.name,
            code=__DEBT_TO_PENNY.code,
            date=datetime.strptime(key, "%Y-%m-%d").date(),
            value1=value,
            value1_name="Total Public Debt Outstanding",
            perc_change1=perc_change,
        ))

        prev_value = value

    return output_data
