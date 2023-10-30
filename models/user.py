from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.subscription import Subcriptions
from models.playstate import Playstate
from typing import List


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    discordId: Mapped[int] = mapped_column(nullable=False)
    subcriptions: Mapped[List[Subcriptions]] = relationship()
    playstates: Mapped[List[Playstate]] = relationship()
