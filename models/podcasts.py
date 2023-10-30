from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class Podcast(Base):
    __tablename__ = "podcast"
    id: Mapped[int] = mapped_column(primary_key=True)
    userId: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    url: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str]
    latestTimeStamp: Mapped[int] = mapped_column(nullable=True)
