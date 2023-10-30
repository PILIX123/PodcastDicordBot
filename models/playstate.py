from models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Playstate(Base):
    __tablename__ = "playstates"
    id: Mapped[int] = mapped_column(primary_key=True)
    userId: Mapped[int] = mapped_column(ForeignKey("users.id"))
    episodeId: Mapped[int] = mapped_column(ForeignKey("episodes.id"))
    timestamp: Mapped[int] = mapped_column(nullable=True)
