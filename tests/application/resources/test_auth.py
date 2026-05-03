from application.resources.auth import (
    get_password_hash,
    verify_password,
    pwd_context,
    oauth2_scheme,
)


class TestGetPasswordHash:
    def test_hash_is_not_plaintext(self) -> None:
        plain: str = "super-secret"
        hashed: str = get_password_hash(plain)
        assert hashed != plain
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_two_hashes_for_same_password_differ(self) -> None:
        a: str = get_password_hash("same")
        b: str = get_password_hash("same")
        assert a != b


class TestVerifyPassword:
    def test_correct_password_verifies(self) -> None:
        hashed: str = get_password_hash("hello")
        assert verify_password("hello", hashed) is True

    def test_wrong_password_does_not_verify(self) -> None:
        hashed: str = get_password_hash("hello")
        assert verify_password("not-hello", hashed) is False


class TestPwdContext:
    def test_uses_bcrypt_scheme(self) -> None:
        assert "bcrypt" in pwd_context.schemes()


class TestOauth2Scheme:
    def test_token_url_is_token(self) -> None:
        assert oauth2_scheme.model.flows.password.tokenUrl == "token"
