import datetime
from typing import List, Optional

from pydantic import BaseModel, field_validator

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

    @field_validator("name")
    def restrict_sortable_fields(cls, value):
        allowed_max_length = 28
        allowed_min_length = 3

        if not allowed_min_length <= len(value) <= allowed_max_length:
            raise ValueError(
                f"len may only: >={allowed_min_length}, <={allowed_max_length} "
            )

        return value

    @field_validator("description")
    def restrict_sortable_fields(cls, value):
        allowed_max_length = 1000
        allowed_min_length = 0

        if not allowed_min_length <= len(value) <= allowed_max_length:
            raise ValueError(
                f"len may only: >={allowed_min_length}, <={allowed_max_length} "
            )

        return value

    @field_validator("date_of_birth")
    def restrict_sortable_fields(cls, value):
        allowed_min_date = datetime.date(1900, 1, 1)

        if not value >= allowed_min_date:
            raise ValueError(f"date may only: >={allowed_min_date}")

        return value

    class Config:
        use_enum_values = True


class PetDetail(Pet):
    id: int
    age: int
    sex: GENDERS
    photos: Optional[List[PhotoDetail]]
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
    total_elements: int
