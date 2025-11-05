from django.db import transaction

from .aus import populate_aus_db
from .usa import populate_usa_db


def populate_db():
    with transaction.atomic():
        try:
            populate_usa_db()
            populate_aus_db()
        except Exception as e:
            transaction.set_rollback(True)
            raise e