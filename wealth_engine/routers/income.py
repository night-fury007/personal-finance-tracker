from typing import List, Sequence, Any, Optional

from fastapi import APIRouter, Depends, status, Response
from sqlmodel import Session

from wealth_engine.common.pginated_response import PaginatedResponse
from wealth_engine.core.dependencies import AuthenticatedUser, get_current_active_user
from wealth_engine.core.exceptions import NotFoundException
from wealth_engine.database import get_db
from wealth_engine.models import Income
from wealth_engine.schemas.income_schema import IncomeCreate, IncomeUpdate, IncomeResponse
from wealth_engine.services.income_service import IncomeService

router = APIRouter(prefix="/api/v1/incomes", tags=["Income"])


@router.post("/", response_model=IncomeResponse, status_code=status.HTTP_201_CREATED)
def create_income(
        income_in: IncomeCreate,
        db: Session = Depends(get_db),
        # current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> Optional[IncomeResponse]:
    return IncomeService.create_income(db=db, user_id="1", income_in=income_in)


@router.get("/", response_model=List[IncomeResponse])
def get_user_incomes(
        page: int = 1,
        limit: int = 10,
        db: Session = Depends(get_db),
        # current_user: AuthenticatedUser = Depends(get_current_active_user)
) -> PaginatedResponse[IncomeResponse]:
    paginated_response = IncomeService.get_incomes_by_user(db=db, user_id="1", page=page, limit=limit)
    if paginated_response.total == 0:
        raise NotFoundException(message="No income found for the user")
    return paginated_response

# @router.get("/searchFilter", response_model=PaginatedResponse[AccountResponse])
# def get_accounts(
#         page: int = 0,
#         limit: int = 10,
#         search: Optional[str] = None,
#         account_type: Optional[str] = None,
#         db: Session = Depends(get_db),
#         # current_user: AuthenticatedUser = Depends(get_current_active_user)
# ) -> PaginatedResponse[AccountResponse]:
#     search_filter_response = AccountService.get_account_by_search_or_filter(
#         db=db,
#         user_id=1,
#         page=page,
#         limit=limit,
#         search=search,
#         account_type=account_type
#     )
#     if search_filter_response.total == 0:
#         raise NotFoundException(message="Account not found")
#     return search_filter_response

# @router.get("/categories", response_model=List[AccountCategoryResponse])
# def get_account_categories(
#         db: Session = Depends(get_db),
#         # current_user: AuthenticatedUser = Depends(get_current_active_user)
# ) -> List[AccountCategoryResponse]:
#     categories = AccountService.get_all_categories(db=db)
#     if not categories:
#         raise NotFoundException(message="No account categories found")
#     return categories

# @router.get("/summary", response_model=AccountSummaryResponse)
# def get_accounts_summary(
#     db: Session = Depends(get_db),
#     # current_user: UsAuthenticatedUserer = Depends(get_current_active_user),
# ) -> AccountSummaryResponse:
#     account_response = AccountService.get_account_summary(db=db, user_id="1")
#     if account_response is None:
#         raise NotFoundException(message="Account not found")
#     return account_response

# @router.get("/{income_id}", response_model=IncomeResponse)
# def get_income(
#         income_id: int,
#         db: Session = Depends(get_db),
#         current_user: AuthenticatedUser = Depends(get_current_active_user)
# ) -> Optional[Any]:
#     """
#     Retrieves a specific income record by ID with tenant security checks.
#     """
#     return IncomeService.get_income_by_id(db=db, income_id=income_id, user_id=current_user.id)
#
#
# @router.put("/{income_id}", response_model=IncomeResponse)
# def update_income(
#         income_id: int,
#         income_in: IncomeUpdate,
#         db: Session = Depends(get_db),
#         current_user: AuthenticatedUser = Depends(get_current_active_user)
# ) -> Income:
#     """
#     Updates an existing income record securely.
#     """
#     return IncomeService.update_income(db=db, income_id=income_id, user_id=current_user.id, income_in=income_in)
#
#
# @router.delete("/{income_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_income(
#         income_id: int,
#         db: Session = Depends(get_db),
#         current_user: AuthenticatedUser = Depends(get_current_active_user)
# ) -> Response:
#     """
#     Deletes an income record securely.
#     """
#     IncomeService.delete_income(db=db, income_id=income_id, user_id=current_user.id)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
