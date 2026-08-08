from typing import Any, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from sqlmodel import Session
from wealth_engine.database import get_db
from wealth_engine.models import User
from wealth_engine.core.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> Optional[Any]:
    """
    Decodes JWT token and retrieves the raw user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    statement = db.query(User).filter(User.email == email)  # or select equivalent
    # Alternatively using select(User).where(User.email == email)
    from sqlmodel import select
    user = db.exec(select(User).where(User.email == email)).first()
    if user is None:
        raise credentials_exception
    return user


class AuthenticatedUser:
    """
    Strict domain wrapper for an authenticated tenant user.
    Guarantees that `id` is strictly a non-nullable integer to static analyzers.
    """

    def __init__(self, user: User):
        if user.id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user session: ID missing"
            )
        self.id: int = user.id  # Strictly enforced int!
        self.email: str = user.email
        self.is_active: bool = user.is_active
        self.raw_user: User = user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> AuthenticatedUser:
    """
    FastAPI dependency injection provider that returns a strictly typed AuthenticatedUser.
    """
    return AuthenticatedUser(current_user)
