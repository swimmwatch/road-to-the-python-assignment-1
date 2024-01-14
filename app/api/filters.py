from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from db.models import Pet

# from pydantic.functional_validators import field_validator


class PetFilter(Filter):
    # order_by: Optional[List[str]]
    name__like: Optional[str]
    description__like: Optional[str]

    # @field_validator("order_by")
    # def restrict_sortable_fields(cls, value):
    #     if value is None:
    #         return None

    #     allowed_field_names = ["created", "date_of_birth"]

    #     for field_name in value:
    #         field_name = field_name.replace("+", "").replace("-", "")
    #         if field_name not in allowed_field_names:
    #             raise ValueError(
    #                 f"You may only sort by: {', '.join(allowed_field_names)}"
    #             )

    #     return value

    # не знаю как корректно сделать ограничение полей orderby и не понимаю почему свагер выдает бесконечную загрузку
    class Constants(Filter.Constants):
        model = Pet
