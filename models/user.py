from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.podcasts import Podcast
from typing import List


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    podcasts: Mapped[List[Podcast]] = relationship()
