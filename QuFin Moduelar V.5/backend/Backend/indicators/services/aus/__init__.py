from typing import List

from . import fred_stlouisfed, oecd_org

from indicators.schemas import EntrySchema


def get_entries() -> List[EntrySchema]:
    return [
        *fred_stlouisfed.get_entries(),
        *oecd_org.get_entries(),
    ]
