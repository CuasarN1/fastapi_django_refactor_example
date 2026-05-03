import inspect
import io
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator


class AsyncCallRecorder:
    """Records await-calls and returns or raises a configured value."""

    def __init__(
        self,
        return_value: Any = None,
        side_effect: Any = None,
    ) -> None:
        self.return_value: Any = return_value
        self.side_effect: Any = side_effect
        self.calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.calls.append((args, kwargs))
        side_effect: Any = self.side_effect
        if side_effect is not None:
            if isinstance(side_effect, BaseException):
                raise side_effect
            if isinstance(side_effect, type) and issubclass(side_effect, BaseException):
                raise side_effect()
            if callable(side_effect):
                result: Any = side_effect(*args, **kwargs)
                if inspect.iscoroutine(result):
                    return await result
                return result
        return self.return_value

    @property
    def call_count(self) -> int:
        return len(self.calls)

    def assert_awaited_once(self) -> None:
        if self.call_count != 1:
            raise AssertionError(
                f"Expected exactly one await, got {self.call_count}"
            )


class FakeRepo:
    """Fake repository with get/create call recorders that tests can replace."""

    def __init__(self) -> None:
        self.get: AsyncCallRecorder = AsyncCallRecorder()
        self.create: AsyncCallRecorder = AsyncCallRecorder()


class FakeSession:
    """Stand-in for an SQLAlchemy AsyncSession.

    The use cases never touch session methods directly — they pass it to the
    repo (which is also faked), so the session only needs to exist and offer
    commit/rollback hooks for completeness.
    """

    def __init__(self) -> None:
        self.commit_calls: int = 0
        self.rollback_calls: int = 0

    async def commit(self) -> None:
        self.commit_calls += 1

    async def rollback(self) -> None:
        self.rollback_calls += 1


class FakeDatabase:
    """Provides an async-context-manager .session() yielding the given FakeSession."""

    def __init__(self, session: FakeSession) -> None:
        self._session: FakeSession = session

    @asynccontextmanager
    async def session(self) -> AsyncIterator[FakeSession]:
        yield self._session


class FakeRow:
    """Simple attribute container compatible with pydantic .model_validate()."""

    def __init__(self, **attrs: Any) -> None:
        for key, value in attrs.items():
            setattr(self, key, value)


class FakeUploadFile:
    """Stand-in for fastapi.UploadFile carrying just .filename and .file."""

    def __init__(self, filename: str, content: bytes = b"data") -> None:
        self.filename: str = filename
        self.file: io.BytesIO = io.BytesIO(content)
