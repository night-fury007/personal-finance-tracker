from decimal import Decimal, ROUND_HALF_UP
from typing import Annotated
from pydantic import BeforeValidator


def round_currency(v):
    if v is None or v == "":
        return Decimal("0.00")
    try:
        return Decimal(str(v)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (ValueError, TypeError):
        return Decimal("0.00")


CurrencyDecimal = Annotated[Decimal, BeforeValidator(round_currency)]
