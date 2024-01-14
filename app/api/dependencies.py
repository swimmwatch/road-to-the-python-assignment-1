from fastapi import HTTPException, Security, status

from db.client import get_session
from db.dal.pet import PetDAL
from db.dal.photo import PhotoDAL

from .config import ApiSettings
from .headers import api_key_header


def get_petdal():
    with get_session() as session:
        return PetDAL(session)


def get_photodal():
    with get_session() as session:
        return PhotoDAL(session)


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header == ApiSettings().api_key:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
