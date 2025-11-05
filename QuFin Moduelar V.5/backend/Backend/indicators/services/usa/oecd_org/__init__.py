from typing import List

from indicators.schemas import EntrySchema

from . import service


def get_entries() -> List[EntrySchema]:
    return [*service.get_entries()]
