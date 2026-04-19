from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from application.infrastructure.sqlite.database import Base


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.login", ondelete="CASCADE", onupdate="CASCADE"))
    image_path: Mapped[str] = mapped_column(nullable=True)
