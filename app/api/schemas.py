import datetime
from typing import List, Optional

from pydantic import BaseModel

from utils.sql.types import GENDERS


class PhotoDetail(BaseModel):
    id: int
    url: str
    pet_id: int
    created: datetime.date

    class Config:
        from_attributes = True


class Pet(BaseModel):
    name: str
    kind: str
    sex: GENDERS
    date_of_birth: datetime.date
    date_of_death: Optional[datetime.date]
    description: Optional[str]

    class Config:
        use_enum_values = True


class PetDetail(Pet):
    id: int
    age: int
    sex: GENDERS
    photos: Optional[list]
    created: datetime.date
    updated: Optional[datetime.date]

    class Config:
        from_attributes = True
        use_enum_values = True


class PetCreate(Pet):
    pass


class PetPatch(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[datetime.date] = None
    date_of_death: Optional[datetime.date] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class PetPaginatedResponse(BaseModel):
    result: List[PetDetail]
    prev_page: Optional[int]
    next_page: Optional[int]
    total_pages: int
