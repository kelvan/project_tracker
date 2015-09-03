import calendar
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


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


def datify(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def get_date_range(first_date, **args):
    today = date.today()

    if args.get('today', False):
        return (today, today)

    if args.get('week', False):
        return _get_current_week_range()

    if args.get('cmonth', False):
        return _get_current_month_range()

    start_date = args.get('from', None)
    end_date = args.get('to', None)

    if start_date or end_date:
        if start_date:
            start_date = datify(start_date)
        else:
            start_date = first_date

        if end_date:
            end_date = datify(end_date)
        else:
            end_date = today

        return (start_date, end_date)

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
        # Does not support future dates
        if d > today:
            last_month = today - relativedelta(months=1)
            d = date(last_month.year, last_month.month, day)
        return (d, d)
