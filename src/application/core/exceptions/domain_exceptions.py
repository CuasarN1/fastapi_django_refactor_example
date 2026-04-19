class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class UserNotFoundByLoginException(BaseDomainException):
    _exception_text_template = "Пользователь с логином='{login}' не найден"

    def __init__(self, login: str) -> None:
        self._exception_text_template = self._exception_text_template.format(login=login)

        super().__init__(detail=self._exception_text_template)


class UserLoginIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с логином='{login}' уже существует"

    def __init__(self, login: str) -> None:
        self._exception_text_template = self._exception_text_template.format(login=login)

        super().__init__(detail=self._exception_text_template)


class WrongPasswordException(BaseDomainException):
    _exception_text = "Неверный пароль"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text)


class UploadFileIsNotImageException(BaseDomainException):
    _exception_text = "Загруженный файл не является JPEG изображением"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text)


class PostHasNoImageException(BaseDomainException):
    _exception_text = "Данный пост не содержит изображения"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text)


class PostNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пост с id='{id}' не найден"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)
