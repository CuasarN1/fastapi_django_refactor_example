from domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from domain.user.use_cases.create_user import CreateUserUseCase

from domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase


def get_get_user_by_login_use_case() -> GetUserByLoginUseCase:
    return GetUserByLoginUseCase()


def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()


def authenticate_user_use_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase()


def create_access_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()
