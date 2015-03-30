import calendar
from datetime import date, timedelta


def in_range(date_, date_range):
    """ check if date_ is in given range (inclusive)
    """
    return date_ >= date_range[0] and date_ <= date_range[1]


def _get_first_day_of_week(year, week):
    day = date(year, 2, 1)
    year, week_base, day_base = day.isocalendar()
    day += timedelta(1 - day_base + (week - week_base)*7)
    return day


def _get_week_range(year, week):
    first_dow = _get_first_day_of_week(year, week)
    return (first_dow, first_dow + timedelta(6))


def _get_current_week_range():
    today = date.today()
    week = today.isocalendar()[1]
    return _get_week_range(today.year, week)


def _get_month_range(year, month):
    first_dom = date(year, month, 1)
    last_dom = date(year, month, calendar.monthrange(year, month)[1])
    return (first_dom, last_dom)


def _get_current_month_range():
    today = date.today()
    return _get_month_range(today.year, today.month)


def _get_year_range(year):
    return (date(year, 1, 1), date(year, 12, 31))


# FIXME day > today.day --> month - 1
def get_date_range(**args):
    today = date.today()

    if args.get('today', False):
        return (today, today)

    if args.get('week', False):
        return _get_current_week_range()

    if args.get('month', False):
        return _get_current_month_range()

    year = args.get('year', None)
    month = args.get('month', None)
    day = args.get('day', None)

    if year is None and month is None and day is None:
        return None

    if year is None:
        year = today.year
    else:
        if year < 1000:
            year += 2000
        if month is None and day is None:
            return _get_year_range(year)

    if month is None:
        month = today.month

    if day is None:
        return _get_month_range(year, month)
    else:
        d = date(year, month, day)
        return (d, d)
