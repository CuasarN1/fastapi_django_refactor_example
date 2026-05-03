from application.core.exceptions.domain_exceptions import (
    BaseDomainException,
    UserNotFoundByLoginException,
    UserLoginIsNotUniqueException,
    WrongPasswordException,
    UploadFileIsNotImageException,
    PostHasNoImageException,
    PostNotFoundByIdException,
)


class TestUserNotFoundByLoginException:
    def test_message_includes_login(self) -> None:
        exc: UserNotFoundByLoginException = UserNotFoundByLoginException(login="alice")
        assert "alice" in exc.get_detail()
        assert "не найден" in exc.get_detail()

    def test_inherits_from_base(self) -> None:
        assert issubclass(UserNotFoundByLoginException, BaseDomainException)


class TestUserLoginIsNotUniqueException:
    def test_message_includes_login(self) -> None:
        exc: UserLoginIsNotUniqueException = UserLoginIsNotUniqueException(login="bob")
        assert "bob" in exc.get_detail()
        assert "уже существует" in exc.get_detail()

    def test_inherits_from_base(self) -> None:
        assert issubclass(UserLoginIsNotUniqueException, BaseDomainException)


class TestWrongPasswordException:
    def test_message(self) -> None:
        assert WrongPasswordException().get_detail() == "Неверный пароль"

    def test_inherits_from_base(self) -> None:
        assert issubclass(WrongPasswordException, BaseDomainException)


class TestUploadFileIsNotImageException:
    def test_message_mentions_jpeg(self) -> None:
        assert "JPEG" in UploadFileIsNotImageException().get_detail()

    def test_inherits_from_base(self) -> None:
        assert issubclass(UploadFileIsNotImageException, BaseDomainException)


class TestPostHasNoImageException:
    def test_message(self) -> None:
        assert "изображения" in PostHasNoImageException().get_detail()

    def test_inherits_from_base(self) -> None:
        assert issubclass(PostHasNoImageException, BaseDomainException)


class TestPostNotFoundByIdException:
    def test_message_includes_id(self) -> None:
        exc: PostNotFoundByIdException = PostNotFoundByIdException(id=42)
        assert "42" in exc.get_detail()
        assert "не найден" in exc.get_detail()

    def test_inherits_from_base(self) -> None:
        assert issubclass(PostNotFoundByIdException, BaseDomainException)
