from datetime import datetime
from typing import List

import httpx

from indicators.schemas import EntrySchema, IndicatorSchema
from indicators.countries import USA

from . import get_last_day_of_the_month


__INTEREST_EXPENSE = IndicatorSchema(
    country=USA,
    code="Interest Exp",
    name="Interest Expense on the Public Debt Outstanding",
    url="https://fiscaldata.treasury.gov/datasets/interest-expense-debt-outstanding/interest-expense-on-the-public-debt-outstanding",
)


def __parse_interest_expense():
    now = get_last_day_of_the_month()

    base_url = "https://api.fiscaldata.treasury.gov/services/api/"\
          "fiscal_service/v2/accounting/od/interest_expense"\
         f"?filter=record_date:gte:2010-05-31,record_date:lte:{now.year}-{now.month}-{now.day}"\
          "&sort=-record_date"

    url = base_url + "&page[number]=1&page[size]=10000"

    response = httpx.get(url)
    data = response.json()["data"]

    sums = {}

    while True:
        for item in data:
            date = item["record_date"]
            month_expense_amt = float(item["month_expense_amt"])
            fytd_expense_amt = float(item["fytd_expense_amt"])

            if date not in sums:
                sums[date] = {"month_expense_amt": 0, "fytd_expense_amt": 0}

            sums[date]["month_expense_amt"] += month_expense_amt
            sums[date]["fytd_expense_amt"] += fytd_expense_amt


        links = response.json()["links"]

        if links["next"] is None:
            break

        next_url = base_url + links["next"]
        response = httpx.get(next_url)
        data = response.json()["data"]
    
    return sums


def get_entries() -> List[EntrySchema]:
    output_data: List[EntrySchema] = []
    data = __parse_interest_expense()

    prev_value1 = None
    prev_value2 = None

    dates = list(data.keys())
    dates.sort()

    for key in dates:
        value1 = data[key]["month_expense_amt"]
        value2 = data[key]["fytd_expense_amt"]

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

        output_data.append(EntrySchema(
            country=__INTEREST_EXPENSE.country,
            name=__INTEREST_EXPENSE.name,
            code=__INTEREST_EXPENSE.code,
            date=datetime.strptime(key, "%Y-%m-%d").date(),
            value1=value1,
            value1_name="Current Month Expense Amount",
            value2=value2,
            value2_name="Fiscal Year to Date Expense Amount",
            perc_change1=perc_change1,
            perc_change2=perc_change2,
        ))

        prev_value1 = value1
        prev_value2 = value2

    return output_data
