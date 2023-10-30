from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from typing import List
from models.episode import Episode
from models.subscription import Subcriptions


class Podcast(Base):
    __tablename__ = "podcasts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    url: Mapped[str] = mapped_column(nullable=False)
    lastEpisode: Mapped[int] = mapped_column(nullable=True)
    subscriptions: Mapped[List[Subcriptions]] = relationship()
    episode: Mapped[List[Episode]] = relationship()
