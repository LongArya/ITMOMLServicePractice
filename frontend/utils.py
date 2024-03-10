from datetime import datetime

SECONDS_IN_DAY = 24 * 60 * 60
FORM_DATE_FORMAT = "%Y-%m-%d"


def get_difference_between_dates_in_days(
    start_date: datetime, end_date: datetime
) -> int:
    time_delta = end_date - start_date
    total_days = time_delta.total_seconds() / SECONDS_IN_DAY
    return int(total_days)


def datetime_from_YYYY_MM_DD(YYYY_MM_DD_repr: str) -> datetime:
    datetime_obj = datetime.strptime(YYYY_MM_DD_repr, FORM_DATE_FORMAT)
    return datetime_obj
