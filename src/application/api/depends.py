from application.domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from application.domain.user.use_cases.create_user import CreateUserUseCase

from application.domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from application.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase

from application.domain.post.use_cases.create_post import CreatePostUseCase
from application.domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from application.domain.post.use_cases.add_post_image import AddPostImageUseCase
from application.domain.post.use_cases.get_post_image import GetPostImageUseCase


def get_get_user_by_login_use_case() -> GetUserByLoginUseCase:
    return GetUserByLoginUseCase()


def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()


def authenticate_user_use_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase()


def create_access_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()


def create_post_use_case() -> CreatePostUseCase:
    return CreatePostUseCase()


def get_post_by_id_use_case() -> GetPostByIdUseCase:
    return GetPostByIdUseCase()


def add_post_image_use_case() -> AddPostImageUseCase:
    return AddPostImageUseCase()


def get_post_image_use_case() -> GetPostImageUseCase:
    return GetPostImageUseCase()
