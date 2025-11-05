from .yahoo_quotes import parse_yahoo_quotes, populate_db_with_yahoo_quotes
from .cot_data import parse_cot_data, populate_db_with_cot


__all__ = [
    "parse_yahoo_quotes",
    "populate_db_with_yahoo_quotes",
    "parse_cot_data",
    "populate_db_with_cot",
    "func"
]

def func():
    populate_db_with_yahoo_quotes(parse_yahoo_quotes())