from .fred_stlouisfed import populate_db_usa_fred_stlouisfed_data
from .oecd_org import populate_db_usa_oecd_org_data


def populate_aus_db():
    populate_db_usa_fred_stlouisfed_data()
    populate_db_usa_oecd_org_data()


__all__ = [
    "populate_db_usa_fred_stlouisfed_data",
    "populate_db_usa_oecd_org_data",
    "populate_aus_db",
]
