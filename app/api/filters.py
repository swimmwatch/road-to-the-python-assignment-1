from typing import List, Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic.functional_validators import field_validator

from db.models import Pet


class PetFilter(Filter):
    order_by: Optional[List[str]] = None
    custom_search: Optional[str] = None
    age__gt: Optional[int] = None
    age__lt: Optional[int] = None

    @field_validator("order_by")
    def restrict_sortable_fields(cls, value):
        if value is None:
            return None

        allowed_field_names = ["created", "date_of_birth"]

        for field_name in value:
            field_name = field_name.replace("+", "").replace("-", "")
            if field_name not in allowed_field_names:
                raise ValueError(
                    f"You may only sort by: {', '.join(allowed_field_names)}"
                )

        return value

    class Constants(Filter.Constants):
        model = Pet
        search_field_name = "custom_search"
        search_model_fields = ["name", "description"]
