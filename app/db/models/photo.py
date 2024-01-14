from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Photo(Base):
    __tablename__ = "photos"
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(nullable=False)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"))
    created: Mapped[date] = mapped_column(default=date.today)
