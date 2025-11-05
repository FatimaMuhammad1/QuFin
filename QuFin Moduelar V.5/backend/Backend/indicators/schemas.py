from datetime import date
from enum import Enum

from pydantic import BaseModel


class Frequency(Enum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    QUARTERLY = 4
    ANNUAL = 5


class CountrySchema(BaseModel):
    code: str
    name: str


class EntrySchema(BaseModel):
    country: CountrySchema
    name: str
    code: str
    date: date
    value1_name: str | None = None
    value1: float | None
    value2_name: str | None = None
    value2: float | None = None
    value3_name: str | None = None
    value3: float | None = None
    total_value: float | None = None
    perc_change1: float
    perc_change2: float | None = None
    perc_change3: float | None = None
    frequency: Frequency = Frequency.MONTHLY
    unit: str | None = None


class IndicatorSchema(BaseModel):
    country: CountrySchema
    name: str
    code: str
    url: str | None
    frequency: Frequency = Frequency.MONTHLY
    file: str | None = None
    unit: str | None = None

    def __hash__(self) -> int:
        return int("".join([str(ord(char)) for char in self.code]))
