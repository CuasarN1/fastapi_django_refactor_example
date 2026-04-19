from typing import Type

from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from application.infrastructure.sqlite.models.users import User as UserModel
from application.schemas.users import CreateUser as UserSchema
from application.core.exceptions.database_exceptions import EntityNotFoundException, EntityAlreadyExistsException


class UserRepository:
    def __init__(self):
        self._model: Type[UserModel] = UserModel

    def get(self, session: Session, login: str) -> UserModel:
        query = (
            select(self._model)
            .where(self._model.login == login)
        )

        user = session.scalar(query)
        if not user:
            raise EntityNotFoundException()

        return user

    def create(self, session: Session, user: UserSchema) -> UserModel:
        query = (
            insert(self._model)
            .values(user.model_dump())
            .returning(self._model)
        )

        try:
            user = session.scalar(query)
        except IntegrityError:
            raise EntityAlreadyExistsException()

        return user
