from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.subscription import Subscriptions
from models.playstate import Playstate
from typing import List


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    subscriptions: Mapped[List[Subscriptions]] = relationship()
    playstates: Mapped[List[Playstate]] = relationship()
    lastPodcastId: Mapped[int] = mapped_column(nullable=True)
    lastEpisodeId: Mapped[int] = mapped_column(nullable=True)
