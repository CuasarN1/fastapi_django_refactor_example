from sqlalchemy.orm import Mapped, mapped_column

from application.infrastructure.sqlite.database import Base


class User(Base):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(primary_key=True, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
