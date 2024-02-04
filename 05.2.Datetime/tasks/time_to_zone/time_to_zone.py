from datetime import datetime

from zoneinfo import ZoneInfo

DEFAULT_TZ_NAME = "Europe/Moscow"


def now() -> datetime:
    """Return now in default timezone"""
    return datetime.now().astimezone(ZoneInfo(DEFAULT_TZ_NAME))


def convert_to_tz(dt: datetime) -> datetime:
    if dt.tzinfo:
        return dt.astimezone(ZoneInfo(DEFAULT_TZ_NAME))
    return dt.replace(tzinfo=ZoneInfo(DEFAULT_TZ_NAME))


def strftime(dt: datetime, fmt: str) -> str:
    """Return dt converted to string according to format in default timezone"""
    return convert_to_tz(dt).strftime(fmt)


def strptime(dt_str: str, fmt: str) -> datetime:
    """Return dt parsed from string according to format in default timezone"""
    return convert_to_tz(datetime.strptime(dt_str, fmt))


def diff(first_dt: datetime, second_dt: datetime) -> int:
    """Return seconds between two datetimes rounded down to closest int"""
    frst = convert_to_tz(first_dt)
    scnd = convert_to_tz(second_dt)

    return int((scnd - frst).total_seconds())


def timestamp(dt: datetime) -> int:
    """Return timestamp for given datetime rounded down to closest int"""
    return int(convert_to_tz(dt).timestamp())


def from_timestamp(ts: float) -> datetime:
    """Return datetime from given timestamp"""
    return datetime.fromtimestamp(ts, ZoneInfo(DEFAULT_TZ_NAME))
