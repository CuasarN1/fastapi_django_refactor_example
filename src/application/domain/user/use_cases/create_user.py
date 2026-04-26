from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.schemas.users import User as UserSchema, CreateUser
from application.core.exceptions.database_exceptions import EntityAlreadyExistsException
from application.core.exceptions.domain_exceptions import UserLoginIsNotUniqueException
from application.resources.auth import get_password_hash


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user: CreateUser) -> UserSchema:
        user.password = get_password_hash(password=user.password)

        try:
            async with self._database.session() as session:
                user = await self._repo.create(session=session, user=user)
        except EntityAlreadyExistsException:
            raise UserLoginIsNotUniqueException(login=user.login)

        return UserSchema.model_validate(obj=user)
