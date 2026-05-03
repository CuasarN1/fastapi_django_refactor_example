from datetime import timedelta, datetime, timezone
from typing import Any

from jose import jwt

from application.core.config import settings
from application.domain.auth.use_cases.create_access_token import (
    CreateAccessTokenUseCase,
)


class TestCreateAccessTokenUseCase:
    async def test_returns_a_decodable_jwt(
        self, create_access_token_use_case: CreateAccessTokenUseCase
    ) -> None:
        token: str = await create_access_token_use_case.execute(login="user_x")

        payload: dict[str, Any] = jwt.decode(
            token,
            key=settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithms=[settings.AUTH_ALGORITHM],
        )
        assert payload["sub"] == "user_x"
        assert "exp" in payload

    async def test_default_expiration_uses_settings(
        self, create_access_token_use_case: CreateAccessTokenUseCase
    ) -> None:
        before: datetime = datetime.now(timezone.utc)
        token: str = await create_access_token_use_case.execute(login="user_x")
        after: datetime = datetime.now(timezone.utc)

        payload: dict[str, Any] = jwt.decode(
            token,
            key=settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithms=[settings.AUTH_ALGORITHM],
        )
        exp: datetime = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        assert before + delta - timedelta(seconds=2) <= exp <= after + delta + timedelta(seconds=2)

    async def test_custom_expiration_is_respected(
        self, create_access_token_use_case: CreateAccessTokenUseCase
    ) -> None:
        custom: timedelta = timedelta(hours=2)
        before: datetime = datetime.now(timezone.utc)
        token: str = await create_access_token_use_case.execute(
            login="user_x", expires_delta=custom
        )
        after: datetime = datetime.now(timezone.utc)

        payload: dict[str, Any] = jwt.decode(
            token,
            key=settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithms=[settings.AUTH_ALGORITHM],
        )
        exp: datetime = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        assert before + custom - timedelta(seconds=2) <= exp <= after + custom + timedelta(seconds=2)
