import logging

from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.schemas.users import User as UserSchema
from application.core.exceptions.database_exceptions import EntityNotFoundException
from application.core.exceptions.domain_exceptions import UserNotFoundByLoginException

logger = logging.getLogger(__name__)


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str, current_user: UserSchema) -> UserSchema:
        try:
            async with self._database.session() as session:
                user = await self._repo.get(session=session, login=login)
        except EntityNotFoundException:
            error = UserNotFoundByLoginException(login=login)
            logger.error(
                f"Пользователь {current_user.login} довел приложение до ошибки: {error.get_detail()}"
            )
            raise error

        return UserSchema.model_validate(obj=user)
