from typing import Literal

from traders_commitment.schemas import CurrencyData


YAHOO_QUOTE_RANGE = Literal["1d", "5d", "1mo", "3mo", "6mo", "1y",
                            "2y", "5y", "10y", "ytd", "max"]


CURRENCIES: list[CurrencyData] = [
    CurrencyData(
        name="EURUSD=X",
        verbose_name="EURO FX - CHICAGO MERCANTILE EXCHANGE"
    ),
    CurrencyData(
        name="JPY=X",
        verbose_name="JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE"
    ),
    CurrencyData(
        name="GBPUSD=X",
        verbose_name="BRITISH POUND - CHICAGO MERCANTILE EXCHANGE"
    ),
    CurrencyData(
        name="AUDUSD=X",
        verbose_name="AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE"
    ),
    CurrencyData(
        name="NZDUSD=X",
        verbose_name="NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE"
    ),
    CurrencyData(
        name="EURJPY=X",
        verbose_name="EURO FX - CHICAGO MERCANTILE EXCHANGE"
    ),
    CurrencyData(
        name="GBPJPY=X",
        verbose_name="BRITISH POUND - CHICAGO MERCANTILE EXCHANGE"
    ),
    CurrencyData(
        name="EURGBP=X",
        verbose_name="EURO FX/BRITISH POUND XRATE - CHICAGO MERCANTILE EXCHANGE"
    ),
    CurrencyData(
        name="EURCAD=X",
        verbose_name="EURO FX - CHICAGO MERCANTILE EXCHANGE"
    ),
    CurrencyData(
        name="EURSEK=X",
        verbose_name="EURO FX - CHICAGO MERCANTILE EXCHANGE"
    ),
    CurrencyData(
        name="EURCHF=X",
        verbose_name="EURO FX - CHICAGO MERCANTILE EXCHANGE"
    ),
    CurrencyData(
        name="EURHUF=X",
        verbose_name="EURO FX - CHICAGO MERCANTILE EXCHANGE"
    ),
    CurrencyData(
        name="MXN=X",
        verbose_name="MEXICAN PESO - CHICAGO MERCANTILE EXCHANGE"
    ),
    CurrencyData(
        name="ZAR=X",
        verbose_name="SO AFRICAN RAND - CHICAGO MERCANTILE EXCHANGE"
    ),
    CurrencyData(
        name="RUB=X",
        verbose_name="RUSSIAN RUBLE - CHICAGO MERCANTILE EXCHANGE"
    )
]