import pytest
from pydantic import ValidationError

from application.schemas.auth import Token


class TestToken:
    def test_valid_token(self) -> None:
        token: Token = Token(access_token="abc.def.ghi", token_type="bearer")
        assert token.access_token == "abc.def.ghi"
        assert token.token_type == "bearer"

    def test_requires_access_token(self) -> None:
        with pytest.raises(ValidationError):
            Token(token_type="bearer")  # type: ignore[call-arg]

    def test_requires_token_type(self) -> None:
        with pytest.raises(ValidationError):
            Token(access_token="abc")  # type: ignore[call-arg]
