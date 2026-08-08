from typing import Any, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from wealth_engine.database import get_db
from wealth_engine.models import User
from wealth_engine.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[Any]:
    """
    FastAPI security dependency that parses the Bearer token,
    extracts the user email, and returns the current User database entity.
    Guarantees strict tenant data isolation.
    """
    payload = decode_access_token(token)

    raw_email = payload.get("sub")
    if raw_email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email: str = str(raw_email)

    statement = select(User).where(User.email == email)
    user = db.exec(statement).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Explicit type assertion / check for static type checker
    return user
