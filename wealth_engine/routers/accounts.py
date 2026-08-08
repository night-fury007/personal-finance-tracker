from typing import List, Sequence, Any, Optional

from fastapi import APIRouter, Depends, status, Response
from sqlmodel import Session

from wealth_engine.core.dependencies import AuthenticatedUser, get_current_active_user
from wealth_engine.database import get_db
from wealth_engine.models import Account
from wealth_engine.schemas.account_schema import AccountCreate, AccountUpdate, AccountResponse
from wealth_engine.services.account_service import AccountService

router = APIRouter(prefix="/api/v1/accounts", tags=["Accounts & Wallets"])


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
        account_in: AccountCreate,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Account:
    """
    Creates a new financial account or wallet for the authenticated tenant user.
    """
    return AccountService.create_account(db=db, user_id=current_user.id, account_in=account_in)


@router.get("/", response_model=List[AccountResponse])
def get_user_accounts(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Sequence[Account]:
    """
    Retrieves all accounts and wallets belonging strictly to the authenticated tenant user.
    """
    return AccountService.get_accounts_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
        account_id: int,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Optional[Any]:
    """
    Retrieves a specific account by ID with tenant security checks.
    """
    return AccountService.get_account_by_id(db=db, account_id=account_id, user_id=current_user.id)


@router.put("/{account_id}", response_model=AccountResponse)
def update_account(
        account_id: int,
        account_in: AccountUpdate,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Optional[Any]:
    """
    Updates an existing account record securely.
    """
    return AccountService.update_account(db=db, account_id=account_id, user_id=current_user.id, account_in=account_in)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
        account_id: int,
        db: Session = Depends(get_db),
        current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Response:
    """
    Deletes an account record securely.
    """
    AccountService.delete_account(db=db, account_id=account_id, user_id=current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
