import calendar
from datetime import date


def get_last_day_of_the_month():
    # Get the current year and month
    current_year = date.today().year
    current_month = date.today().month

    # Get the number of days in the current month
    last_day = calendar.monthrange(current_year, current_month)[1]

    # Create a date object for the last day of the current month
    return date(current_year, current_month, last_day)
