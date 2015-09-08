from daterange import _get_month_range


def get_weekday_count_range(first_weekday, days):
    avg = days // 7
    remainder = days % 7

    if remainder == 0:
        return [avg for i in range(7)]

    remainder_start = max(0, (first_weekday + remainder) - 7)
    count = []
    for i in range(7):
        if (i >= first_weekday and i < first_weekday + remainder) or i < remainder_start:
            count.append(avg+1)
        else:
            count.append(avg)

    return count


def get_weekday_count_month(year, month):
    month = _get_month_range(year, month)
    return get_weekday_count_range(month[0].weekday(), month[1].day)
