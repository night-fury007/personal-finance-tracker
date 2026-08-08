from decimal import Decimal
from sqlmodel import Session, select
from wealth_engine.models import FXRate
from wealth_engine.core.exceptions import DatabaseOperationException


class FXService:
    @staticmethod
    def get_latest_exchange_rate(db: Session, base: str = "USD", target: str = "INR") -> Decimal:
        """
        Retrieves the latest USD to INR exchange rate from the database.
        Falls back to a standard default rate (e.g., 83.00) if none exists.
        """
        try:
            statement = (
                select(FXRate)
                .where(FXRate.base_currency == base, FXRate.target_currency == target)
                .order_by(FXRate.rate_date.desc())
            )
            fx_record = db.exec(statement).first()
            if fx_record:
                return fx_record.rate

            return Decimal("83.00")
        except Exception as e:
            raise DatabaseOperationException(message=f"Failed to fetch exchange rate: {str(e)}") from e
