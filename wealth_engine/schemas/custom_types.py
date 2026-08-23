from decimal import Decimal, ROUND_HALF_UP
from typing import Annotated
from pydantic import BeforeValidator


def round_currency(v) -> Decimal | None:
    if v is None:
        return None
    try:
        return Decimal(str(v)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (TypeError, ValueError):
        return v


CurrencyDecimal = Annotated[Decimal, BeforeValidator(round_currency)]
