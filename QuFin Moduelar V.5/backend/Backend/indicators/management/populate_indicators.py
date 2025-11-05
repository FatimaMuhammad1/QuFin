from django.core.management.base import BaseCommand

from indicators.services.db import populate_db
from indicators.services.usa import get_entries


class Command(BaseCommand):
    help = "Populates the database with initial entries of indicators"

    def handle(self, *args, **options):
        populate_db(entries_data=get_entries())
