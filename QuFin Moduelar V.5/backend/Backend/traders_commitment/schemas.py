from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class CurrencyData(BaseModel):
    name: str
    verbose_name: str

    def __hash__(self):
        return hash((self.name, self.verbose_name))

    def __eq__(self, other):
        return (self.name, self.verbose_name) == (other.name, other.verbose_name)


class CurrencyValueData(BaseModel):
    currency: CurrencyData
    timestamp: date
    open_price: Optional[float]
    close_price: Optional[float]
    high_price: Optional[float]
    low_price: Optional[float]
    adj_close_price: Optional[float]


class CoTFinData(BaseModel):
    currency: CurrencyData
    date: date

    asset_manager_positions_long: Optional[int]
    asset_manager_positions_short: Optional[int]
    asset_manager_positions_long_short: Optional[int] = None

    leverage_money_positions_long: Optional[int]
    leverage_money_positions_short: Optional[int]
    leverage_money_positions_long_short: Optional[int] = None

    other_rept_positions_long_all: Optional[int]
    other_rept_positions_short_all: Optional[int]
    other_rept_positions_long_short_all: Optional[int] = None

    percentage_of_open_interest_asset_manager_long: Optional[int]
    percentage_of_open_interest_asset_manager_short: Optional[int]
    percentage_of_open_interest_asset_manager_long_short: Optional[int] = None

    percentage_of_leverage_money_asset_manager_long: Optional[int]
    percentage_of_leverage_money_asset_manager_short: Optional[int]
    percentage_of_leverage_money_asset_manager_long_short: Optional[int] = None

    percentage_of_other_rept_positions_long_all: Optional[int]
    percentage_of_other_rept_positions_short_all: Optional[int]
    percentage_of_other_rept_positions_long_short_all: Optional[int] = None
