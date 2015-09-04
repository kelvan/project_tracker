from datetime import datetime

from .weekday_count import get_weekday_count_range
from settings import workhours_per_day


def get_workhours(start_date, end_date):
    weekday_count = get_weekday_count_range(start_date.weekday(),
                                            (end_date-start_date).days+1)
    return sum([workhours_per_day[weekday] * count
                for weekday, count in enumerate(weekday_count)])
