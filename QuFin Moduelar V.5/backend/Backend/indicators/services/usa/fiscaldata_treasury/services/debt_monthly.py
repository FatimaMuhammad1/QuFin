from typing import List
from datetime import datetime

import httpx

from indicators.schemas import EntrySchema, IndicatorSchema, Frequency
from indicators.countries import USA

from . import get_last_day_of_the_month

__DEBT_MONTHLY = IndicatorSchema(
    country=USA,
    code="Public Debt (Monthly)",
    name="Schedule of Federal Debt (public & intragovernmental)",
    url="https://fiscaldata.treasury.gov/datasets/schedules-federal-debt/schedules-of-federal-debt-by-month",
    frequency=Frequency.DAILY
)


def __parse_debt_monthly():
    now = get_last_day_of_the_month()

    base_url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/"\
          "accounting/od/schedules_fed_debt?filter=record_date:gte:2005-10-31,"\
         f"record_date:lte:{now.year}-{now.month}-{now.day}&sort=-record_date"
    url = base_url + "&page%5Bnumber%5D=1&page%5Bsize%5D=10000"

    response = httpx.get(url)
    data = response.json()["data"]

    debts = {}

    balance_div = "Balance as of "

    while True:
        for item in data:
            date = item["record_date"]
            if date not in debts:
                debts[date] = {
                    "principal_mil_amt": 0.0,
                    "accrued_int_payable_mil_amt": 0.0,
                    "net_unamortized_mil_amt": 0.0
                }

            if balance_div in item["security_class1_desc"]:
                balance_date = datetime.strptime(
                    item["security_class1_desc"],
                    f"{balance_div}%B %d, %Y"
                ).date().strftime("%Y-%m-%d")

                if balance_date not in debts:
                    debts[balance_date] = {
                        "principal_mil_amt": 0.0,
                        "accrued_int_payable_mil_amt": 0.0,
                        "net_unamortized_mil_amt": 0.0
                    }

                debts[balance_date]["principal_mil_amt"] += int(item["principal_mil_amt"])
                debts[balance_date]["accrued_int_payable_mil_amt"] += int(item["accrued_int_payable_mil_amt"])
                debts[balance_date]["net_unamortized_mil_amt"] += int(item["net_unamortized_mil_amt"])

        links = response.json()["links"]

        if links["next"] is None:
            break

        next_url = base_url + links["next"]
        response = httpx.get(next_url)
        data = response.json()["data"]

    return debts


def get_entries() -> List[EntrySchema]:
    output_data: List[EntrySchema] = []
    data = __parse_debt_monthly()

    prev_value1 = None
    prev_value2 = None
    prev_value3 = None

    dates = list(data.keys())
    dates.sort()

    for key in dates:
        value1 = data[key]["principal_mil_amt"]
        value2 = data[key]["accrued_int_payable_mil_amt"]
        value3 = data[key]["net_unamortized_mil_amt"]

        if prev_value1 not in [None, 0.0]:
            perc_change1 = round(
                (value1 - prev_value1) / prev_value1,
                ndigits=6
            )
        else:
            perc_change1 = 0.0

        if prev_value2 not in [None, 0.0]:
            perc_change2 = round(
                (value2 - prev_value2) / prev_value2,
                ndigits=6
            )
        else:
            perc_change2 = 0.0

        if prev_value3 not in [None, 0.0]:
            perc_change3 = round(
                (value3 - prev_value3) / prev_value3,
                ndigits=6
            )
        else:
            perc_change3 = 0.0
        
        total_value = value1 + value2 + value3

        output_data.append(EntrySchema(
            country=__DEBT_MONTHLY.country,
            name=__DEBT_MONTHLY.name,
            code=__DEBT_MONTHLY.code,
            date=datetime.strptime(key, "%Y-%m-%d").date(),
            total_value=total_value,
            value1=value1,
            value1_name="Principal Amount in Millions",
            perc_change1=perc_change1,
            value2=value2,
            value2_name="Accrued Interest Payable Amount in Millions",
            perc_change2=perc_change2,
            value3=value3,
            value3_name="Net Unamortized Amount in Millions",
            perc_change3=perc_change3,
        ))

        prev_value1 = value1
        prev_value2 = value2
        prev_value3 = value3

    return output_data
