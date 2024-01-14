from typing import Annotated

from fastapi import (APIRouter, Depends, File, HTTPException, Query, Security,
                     UploadFile, status)
from fastapi_filter import FilterDepends
from sqlalchemy import exc

from amazonstorage.config import MinioSettings
from utils.image_convert import (check_format_valid, construct_url_for_image,
                                 convert_format_suffix)
from utils.minio import delete_image_file, get_flow_in_format_and_write

from .config import ImageFormatSettings
from .dependencies import get_api_key, get_petdal, get_photodal
from .filters import PetFilter
from .schemas import (PetCreate, PetDetail, PetPaginatedResponse, PetPatch,
                      PhotoDetail)

router = APIRouter(prefix="/pet")


@router.get("/{pet_id}", response_model=PetDetail)
def get_one_pet(
    pet_id: int, api_key: str = Security(get_api_key), pet_dal=Depends(get_petdal)
):
    one_pet = pet_dal.get_one_or_none(id=pet_id)
    if one_pet is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return one_pet


@router.post("/", response_model=PetDetail)
def create_one_pet(
    operation_data: PetCreate,
    api_key: str = Security(get_api_key),
    pet_dal=Depends(get_petdal),
):
    return pet_dal.create_one(**operation_data.dict())


@router.patch("/{pet_id}", response_model=PetDetail)
def patch_one_pet(
    pet_id: int,
    operation_data: PetPatch,
    api_key: str = Security(get_api_key),
    pet_dal=Depends(get_petdal),
):
    patched_pet = pet_dal.update_one(operation_data.dict(exclude_unset=True), id=pet_id)
    if patched_pet is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return patched_pet


@router.get("/", response_model=PetPaginatedResponse)
def get_pages(
    limit: Annotated[int, Query(ge=1)],
    page: Annotated[int, Query(ge=1)] = 1,
    pet_filter: PetFilter = FilterDepends(PetFilter),
    api_key: str = Security(get_api_key),
    pet_dal=Depends(get_petdal),
):
    filter_query = pet_filter.filter(pet_dal.query())
    # query = pet_filter.sort(filter_query)
    result, prev_page, next_page, total_pages = pet_dal.base(filter_query).fetch(
        limit, page
    )
    return PetPaginatedResponse(
        result=result, prev_page=prev_page, next_page=next_page, total_pages=total_pages
    )


@router.post("/{pet_id}", response_model=PhotoDetail)
async def upload_file(
    pet_id: int,
    file: UploadFile = File(...),
    api_key: str = Security(get_api_key),
    photo_dal=Depends(get_photodal),
):
    if check_format_valid(file.content_type):
        single_format = ImageFormatSettings().single_image_format
        name = convert_format_suffix(file.filename, single_format)
        get_flow_in_format_and_write(file.file, single_format, name)
        url = construct_url_for_image(
            MinioSettings().endpoint, MinioSettings().bucket_name, name
        )
        try:
            return photo_dal.create_one(url=url, pet_id=pet_id)
        except exc.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid pet id"
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file format"
        )


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    pet_id: int,
    file_id: int,
    api_key: str = Security(get_api_key),
    photo_dal=Depends(get_photodal),
):
    result = photo_dal.delete_one(pet_id=pet_id, id=file_id)
    if result:
        delete_image_file(result.url)
        return status.HTTP_204_NO_CONTENT
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file pet_id or photo_id",
        )
