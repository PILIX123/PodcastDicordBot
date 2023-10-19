from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class PodcastList(Base):
    __tablename__ = "list"
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(nullable=False)
    urls:Mapped[str] = mapped_column(nullable=True)