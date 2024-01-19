from datetime import date
from typing import List, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from utils.sql.types import GENDERS


class Pet(Base):
    __tablename__ = "pets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    kind: Mapped[str]
    sex: Mapped[GENDERS]
    date_of_birth: Mapped[date]
    date_of_death: Mapped[Optional[date]]
    description: Mapped[Optional[str]]
    photos: Mapped[Optional[List["Photo"]]] = relationship(cascade="all")
    created: Mapped[date] = mapped_column(default=date.today)
    updated: Mapped[Optional[date]] = mapped_column(onupdate=date.today)

    @hybrid_property
    def age(self):
        if self.date_of_death:
            last_day = self.date_of_death
        else:
            last_day = date.today()
        return (
            last_day.year
            - self.date_of_birth.year
            - (
                (last_day.month, last_day.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )

    @age.inplace.expression
    @classmethod
    def _age_expression(cls):
        return func.extract(
            "year",
            func.age(
                func.coalesce(cls.date_of_death, func.current_date()), cls.date_of_birth
            ),
        )


class Photo(Base):
    __tablename__ = "photos"
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(nullable=False)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"))
    created: Mapped[date] = mapped_column(default=date.today)
