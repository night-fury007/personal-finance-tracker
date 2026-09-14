import uuid
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

DATE_TIME_FORMAT = "%d-%m-%Y-%H:%M:%S"
IST = ZoneInfo("Asia/Kolkata")


def parse_custom_datetime(v: Any) -> None | datetime | str | Any:
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


def generate_public_account_id() -> str:
    """Generates a unique public identifier for entities."""
    return str(uuid.uuid4())


def calculate_page_offset(
        page: int,
        limit: int,
) -> int:
    """Calculates the page offset."""
    return max(0, (page - 1) * limit) if page > 0 else 0
