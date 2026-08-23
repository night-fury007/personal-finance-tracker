from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Annotated, Any
from pydantic import BeforeValidator, PlainSerializer

DATE_TIME_FORMAT = "%d-%m-%Y-%H:%M:%S"
IST = ZoneInfo("Asia/Kolkata")


def parse_custom_datetime(v: Any) -> datetime | None:
    if v is None or isinstance(v, datetime):
        return v
    if isinstance(v, str):
        try:
            return datetime.strptime(v, DATE_TIME_FORMAT)
        except ValueError:
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                pass
    return v


def format_to_ist_string(v: datetime | None) -> str | None:
    """Converts UTC datetime from DB to IST and formats it as 'dd-mm-yyyy-hh:mm:ss'"""
    if v is None:
        return None

    # If the stored datetime is naive (no timezone info), assume it's UTC
    if v.tzinfo is None:
        v = v.replace(tzinfo=ZoneInfo("UTC"))

    # Convert to IST
    ist_datetime = v.astimezone(IST)
    return ist_datetime.strftime(DATE_TIME_FORMAT)


# Your updated reusable type for API responses
CustomDateTimeIST = Annotated[
    datetime,
    BeforeValidator(parse_custom_datetime),
    PlainSerializer(format_to_ist_string, return_type=str | None, when_used="json-unless-none")
]
