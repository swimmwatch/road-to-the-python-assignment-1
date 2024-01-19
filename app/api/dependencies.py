from fastapi import HTTPException, Security, status, Depends

from db.client import get_session
from db.dal.pet import PetDAL
from db.dal.photo import PhotoDAL

from .config import ApiSettings
from .headers import api_key_header


def get_petdal(session = Depends(get_session)):
    with session as db_session:
        return PetDAL(db_session)


def get_photodal(session = Depends(get_session)):
    with session as db_session:
        return PhotoDAL(db_session)


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header == ApiSettings().api_key:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
