from domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from domain.user.use_cases.create_user import CreateUserUseCase


def get_get_user_by_login_use_case() -> GetUserByLoginUseCase:
    return GetUserByLoginUseCase()


def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()
