from db.models import Photo
from utils.sql.dal import SqlAlchemyRepository


class PhotoDAL(SqlAlchemyRepository):
    class Config:
        model = Photo
