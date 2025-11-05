from typing import List
from indicators.schemas import EntrySchema

from . import table_3


def get_entries() -> List[EntrySchema]:
    return [*table_3.get_entries()]
