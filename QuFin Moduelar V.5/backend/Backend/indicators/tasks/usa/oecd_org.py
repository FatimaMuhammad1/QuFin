from core.celery import app

from indicators.services.usa.oecd_org import get_entries
from indicators.services.db import populate_db


@app.task()
def populate_db_usa_oecd_org_data():
    entries = get_entries()
    populate_db(entries_data=entries)
