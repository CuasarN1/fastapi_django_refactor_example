from fastapi import APIRouter, status, HTTPException, Depends

from schemas.users import User, CreateUser
from domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from domain.user.use_cases.create_user import CreateUserUseCase
from api.depends import (
    get_get_user_by_login_use_case,
    create_user_use_case,
)
from core.exceptions.domain_exceptions import UserNotFoundByLoginException, UserLoginIsNotUniqueException
from services.auth import AuthService

router = APIRouter()


@router.get(
    "/{login}",
    status_code=status.HTTP_200_OK,
    response_model=User,
)
async def get_user_by_login(
    login: str,
    user: User = Depends(AuthService.get_current_user),
    use_case: GetUserByLoginUseCase = Depends(get_get_user_by_login_use_case),
) -> User:
    try:
        return await use_case.execute(login=login, current_user=user)
    except UserNotFoundByLoginException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@router.post("", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    user: CreateUser,
    use_case: CreateUserUseCase = Depends(create_user_use_case),
) -> User:
    try:
        return await use_case.execute(user=user)
    except UserLoginIsNotUniqueException as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())
