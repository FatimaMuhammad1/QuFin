from typing import List

from . import fred_stlouisfed, ism, nahb, oecd_org, fiscaldata_treasury

from indicators.schemas import EntrySchema


def get_entries() -> List[EntrySchema]:
    return [
        *fred_stlouisfed.get_entries(),
        *ism.get_entries(),
        *nahb.get_entries(),
        *oecd_org.get_entries(),
        *fiscaldata_treasury.get_entries(),
    ]