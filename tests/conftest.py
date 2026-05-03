from pathlib import Path

import pytest

from application.domain.auth.use_cases.authenticate_user import (
    AuthenticateUserUseCase,
)
from application.domain.auth.use_cases.create_access_token import (
    CreateAccessTokenUseCase,
)
from application.domain.post.use_cases.add_post_image import AddPostImageUseCase
from application.domain.post.use_cases.create_post import CreatePostUseCase
from application.domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from application.domain.post.use_cases.get_post_image import GetPostImageUseCase
from application.domain.user.use_cases.create_user import CreateUserUseCase
from application.domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from application.schemas.users import User

from tests.mocks import FakeDatabase, FakeRepo, FakeSession


# ---------------------------------------------------------------------------
# Database / session fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def fake_session() -> FakeSession:
    return FakeSession()


@pytest.fixture
def fake_database(fake_session: FakeSession) -> FakeDatabase:
    return FakeDatabase(fake_session)


# ---------------------------------------------------------------------------
# Domain fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def current_user() -> User:
    return User(login="user_caller", password="hashed")


# ---------------------------------------------------------------------------
# Auth use case fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def authenticate_user_use_case(fake_database: FakeDatabase) -> AuthenticateUserUseCase:
    uc: AuthenticateUserUseCase = AuthenticateUserUseCase()
    uc._database = fake_database
    uc._repo = FakeRepo()
    return uc


@pytest.fixture
def create_access_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()


# ---------------------------------------------------------------------------
# User use case fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def get_user_by_login_use_case(fake_database: FakeDatabase) -> GetUserByLoginUseCase:
    uc: GetUserByLoginUseCase = GetUserByLoginUseCase()
    uc._database = fake_database
    uc._repo = FakeRepo()
    return uc


@pytest.fixture
def create_user_use_case(fake_database: FakeDatabase) -> CreateUserUseCase:
    uc: CreateUserUseCase = CreateUserUseCase()
    uc._database = fake_database
    uc._repo = FakeRepo()
    return uc


# ---------------------------------------------------------------------------
# Post use case fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def create_post_use_case(fake_database: FakeDatabase) -> CreatePostUseCase:
    uc: CreatePostUseCase = CreatePostUseCase()
    uc._database = fake_database
    uc._repo = FakeRepo()
    return uc


@pytest.fixture
def get_post_by_id_use_case(fake_database: FakeDatabase) -> GetPostByIdUseCase:
    uc: GetPostByIdUseCase = GetPostByIdUseCase()
    uc._database = fake_database
    uc._repo = FakeRepo()
    return uc


@pytest.fixture
def add_post_image_use_case(tmp_path: Path) -> AddPostImageUseCase:
    uc: AddPostImageUseCase = AddPostImageUseCase()
    uc.image_folder = str(tmp_path)
    return uc


@pytest.fixture
def get_post_image_use_case(
    fake_database: FakeDatabase, tmp_path: Path
) -> GetPostImageUseCase:
    uc: GetPostImageUseCase = GetPostImageUseCase()
    uc._database = fake_database
    uc._repo = FakeRepo()
    uc.image_folder = str(tmp_path)
    return uc
