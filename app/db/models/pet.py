from datetime import date
from typing import List, Optional

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

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

    @validates("name")
    def validate_name(self, key, name) -> str:
        if len(name) < 3 or len(name) > 28:
            raise ValueError("name not correct")
        return name

    @validates("description")
    def validate_description(self, key, description) -> str:
        if len(description) > 1024:
            raise ValueError("description not correct")
        return description

    @validates("date_of_birth")
    def validate_date_of_birth(self, key, date_of_birth) -> date:
        if date_of_birth < date(1900, 1, 1):
            raise ValueError("date_of_birth not correct")
        return date_of_birth

    @hybrid_property
    def age(self):
        if self.date_of_death:
            deltaa = self.date_of_death - self.date_of_birth
        else:
            deltaa = date.today() - self.date_of_birth
        age = int(deltaa.days) // 365
        return age
