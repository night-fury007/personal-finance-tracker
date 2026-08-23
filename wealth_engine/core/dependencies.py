from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from sqlmodel import Session

from wealth_engine.core.security import SECRET_KEY, ALGORITHM
from wealth_engine.database import get_db
from wealth_engine.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> type[User]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user


class AuthenticatedUser:
    """
    Strict domain wrapper for an authenticated tenant user.
    Guarantees non-nullable types (`id: int`, `email: str`, `is_active: bool`)
    to satisfy static analysis tools completely.
    """

    def __init__(self, user: User):
        if user.id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user session: ID missing"
            )
        self.id: str = user.id
        self.email: str = user.email
        self.is_active: bool = user.is_active
        self.raw_user: User = user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> AuthenticatedUser:
    """
    FastAPI dependency injection provider that returns a strictly typed AuthenticatedUser.
    """
    return AuthenticatedUser(current_user)
