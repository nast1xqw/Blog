from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text



class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(
        primary_key = True,
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable = False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable = False,
    )