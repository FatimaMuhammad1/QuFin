from typing import List

from indicators.schemas import EntrySchema

from .services import interest_expense, debt_penny, debt_monthly


def get_entries() -> List[EntrySchema]:
    return [
        *interest_expense.get_entries(),
        *debt_penny.get_entries(),
        *debt_monthly.get_entries()
    ]