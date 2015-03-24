import calendar
from datetime import date, timedelta


def in_range(date_, date_range):
    return date_ >= date_range[0] and date_ <= date_range[1]


def _get_first_day_of_week(year, week):
    day = date(year, 2, 1)
    year, week_base, day_base = day.isocalendar()
    day += timedelta(1 - day_base + (week - week_base)*7)
    return day


def _get_week_range(year=None, week=None):
    first_dow = _get_first_day_of_week(year, week)
    return (first_dow, first_dow + timedelta(6))


def _get_current_week_range():
    today = date.today()
    week = today.isocalendar()[1]
    return _get_week_range(today.year, week)


def _get_year_range(year):
    return (date(year, 1, 1), date(year, 12, 31))


def get_date_range(**args):
    print(args)

    if args.get('today', False):
        today = date.today()
        return (today, today)

    if args.get('week', False):
        return _get_current_week_range()
