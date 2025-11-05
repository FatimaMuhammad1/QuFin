from core.celery import app

from indicators.services.aus.fred_stlouisfed import get_entries
from indicators.services.db import populate_db


@app.task()
def populate_db_usa_fred_stlouisfed_data():
    entries = get_entries()
    populate_db(entries_data=entries)
