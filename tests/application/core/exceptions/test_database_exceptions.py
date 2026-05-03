import pytest

from application.core.exceptions.database_exceptions import (
    BaseDatabaseException,
    EntityNotFoundException,
    EntityAlreadyExistsException,
)


class TestEntityNotFoundException:
    def test_inherits_from_base(self) -> None:
        assert issubclass(EntityNotFoundException, BaseDatabaseException)

    def test_can_be_raised_and_caught(self) -> None:
        with pytest.raises(EntityNotFoundException):
            raise EntityNotFoundException()

    def test_accepts_optional_detail(self) -> None:
        EntityNotFoundException()
        EntityNotFoundException(detail="missing")


class TestEntityAlreadyExistsException:
    def test_inherits_from_base(self) -> None:
        assert issubclass(EntityAlreadyExistsException, BaseDatabaseException)

    def test_can_be_raised_and_caught(self) -> None:
        with pytest.raises(EntityAlreadyExistsException):
            raise EntityAlreadyExistsException()
