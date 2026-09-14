from datetime import datetime
from typing import Annotated, Any
from pydantic import BeforeValidator, PlainSerializer

from wealth_engine.common.utils import parse_custom_datetime, format_to_ist_string

CustomDateTimeIST = Annotated[
    datetime,
    BeforeValidator(parse_custom_datetime),
    PlainSerializer(format_to_ist_string, return_type=str | None, when_used="json-unless-none")
]
