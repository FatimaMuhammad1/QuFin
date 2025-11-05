from .fred_stlouisfed import populate_db_usa_fred_stlouisfed_data
from .ism import populate_db_usa_ism_data
from .nahb import populate_db_usa_nahb_data
from .oecd_org import populate_db_usa_oecd_org_data
from .fiscaldata_treasury import populate_db_usa_fiscaldata_treasury_data

# from indicators.tasks.usa import populate_db_usa_nahb_data
# from indicators.tasks.usa import populate_db_usa_oecd_org_data


def populate_usa_db():
    populate_db_usa_fred_stlouisfed_data()
    populate_db_usa_ism_data()
    populate_db_usa_nahb_data()
    populate_db_usa_oecd_org_data()
    populate_db_usa_fiscaldata_treasury_data()


__all__ = [
    "populate_db_usa_fred_stlouisfed_data",
    "populate_db_usa_ism_data",
    "populate_db_usa_nahb_data",
    "populate_db_usa_oecd_org_data",
    "populate_db_usa_fiscaldata_treasury_data",
    "populate_usa_db"
]