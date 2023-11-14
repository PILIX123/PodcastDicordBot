from models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Episode(Base):
    __tablename__ = "episodes"
    id: Mapped[int] = mapped_column(primary_key=True)
    podcastId: Mapped[int] = mapped_column(ForeignKey("podcasts.id"))
    episodeNumber: Mapped[int]
    title: Mapped[str] = mapped_column(nullable=True)
