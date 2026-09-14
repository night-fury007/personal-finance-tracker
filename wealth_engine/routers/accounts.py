from typing import Optional, List

from fastapi import APIRouter, Depends, status, Response
from sqlmodel import Session

from wealth_engine.common.pginated_response import PaginatedResponse
from wealth_engine.core.exceptions import NotFoundException
from wealth_engine.database import get_db
from wealth_engine.schemas.account_schema import AccountCreate, AccountUpdate, AccountResponse, AccountCategoryResponse, \
    AccountSummaryResponse
from wealth_engine.services.account_service import AccountService

router = APIRouter(prefix="/api/v1/accounts", tags=["Accounts & Wallets"])


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
        account_in: AccountCreate,
        db: Session = Depends(get_db)
        # current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Optional[AccountResponse]:
    return AccountService.create_account(db=db, user_id="1", account_in=account_in)


@router.get("/", response_model=PaginatedResponse[AccountResponse])
def get_user_accounts(
        page: int = 1,
        limit: int = 10,
        db: Session = Depends(get_db)
        # current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> PaginatedResponse[AccountResponse]:
    paginated_response = AccountService.get_accounts_by_user(db=db, user_id="1", page=page, limit=limit)
    if paginated_response.total == 0:
        raise NotFoundException(message="No account found for the user")
    return paginated_response


@router.get("/searchFilter", response_model=PaginatedResponse[AccountResponse])
def get_accounts(
        page: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
        account_type: Optional[str] = None,
        db: Session = Depends(get_db),
        # current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> PaginatedResponse[AccountResponse]:
    search_filter_response = AccountService.get_account_by_search_or_filter(
        db=db,
        user_id=1,
        page=page,
        limit=limit,
        search=search,
        account_type=account_type
    )
    if search_filter_response.total == 0:
        raise NotFoundException(message="Account not found")
    return search_filter_response


@router.get("/categories", response_model=List[AccountCategoryResponse])
def get_account_categories(
        db: Session = Depends(get_db),
        # current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> List[AccountCategoryResponse]:
    categories = AccountService.get_all_categories(db=db)
    if not categories:
        raise NotFoundException(message="No account categories found")
    return categories

@router.get("/summary", response_model=AccountSummaryResponse)
def get_accounts_summary(
    db: Session = Depends(get_db),
    # current_user: UsAuthenticatedUserer = Depends(get_current_active_user),
) -> AccountSummaryResponse:
    account_response = AccountService.get_account_summary(db=db, user_id="1")
    if account_response is None:
        raise NotFoundException(message="Account not found")
    return account_response

@router.get("/{public_account_id}", response_model=AccountResponse)
def get_account(
        public_account_id: str,
        db: Session = Depends(get_db),
        # current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> AccountResponse:
    account_response = AccountService.get_account_by_id(db=db, public_account_id=public_account_id, user_id=1)
    if account_response is None:
        raise NotFoundException(message="Account not found")
    return account_response


@router.put("/{public_account_id}", response_model=AccountResponse)
def update_account(
        account_in: AccountUpdate,
        db: Session = Depends(get_db),
        # current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Optional[AccountResponse]:
    account_response = AccountService.update_account(db=db, user_id=1, account_in=account_in)
    if account_response is None:
        raise NotFoundException(message="Account not found")
    return account_response


@router.delete("/{public_account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
        public_account_id: str,
        db: Session = Depends(get_db),
        # current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> None:
    AccountService.delete_account(db=db, public_account_id=public_account_id, user_id=1)
