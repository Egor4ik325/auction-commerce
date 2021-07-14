from datetime import timedelta, timezone, datetime


def current_datetime():
    """Get current date and time with timezone offset."""
    msk_tz = timezone(timedelta(hours=3), 'MSK')
    cur_dt = datetime.now(tz=msk_tz)
    return cur_dt


def current_datetime_string():
    """Get current datetime str formatted."""
    cur_dt = current_datetime()
    cur_dt_str = cur_dt.strftime('%Y-%m-%d %H:%M')
    return cur_dt_str


def current_date_string():
    """Get current date str formatted."""
    cur_dt = current_datetime()
    cur_date_str = cur_dt.strftime('%Y-%m-%d')
    return cur_date_str


def current_time_string():
    """Get current time str formatted."""
    cur_dt = current_datetime()
    cur_time_str = cur_dt.strftime('%H:%M')
    return cur_time_str
