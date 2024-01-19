from db.models import Pet
from utils.sql.dal import SqlAlchemyRepository


class PetDAL(SqlAlchemyRepository):
    class Config:
        model = Pet
