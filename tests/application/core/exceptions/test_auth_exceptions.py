from fastapi import HTTPException

from application.core.exceptions.auth_exceptions import CredentialsException


class TestCredentialsException:
    def test_inherits_from_http_exception(self) -> None:
        assert issubclass(CredentialsException, HTTPException)

    def test_status_code_is_401(self) -> None:
        exc: CredentialsException = CredentialsException(detail="bad creds")
        assert exc.status_code == 401

    def test_detail_is_propagated(self) -> None:
        exc: CredentialsException = CredentialsException(detail="bad creds")
        assert exc.detail == "bad creds"

    def test_sets_www_authenticate_header(self) -> None:
        exc: CredentialsException = CredentialsException(detail="bad creds")
        assert exc.headers == {"WWW-Authenticate": "Bearer"}
