import alembic.command
import alembic.config
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database

from app.api.config import ApiSettings
from app.api.dependencies import get_petdal
from app.api.main import app
from app.db.config import DatabaseSettings
from app.db.dal.pet import PetDAL


@pytest.fixture(scope="function")
def pet_repo(create_session):
    return PetDAL(create_session)


@pytest.fixture(scope="function")
def client(pet_repo):
    app.dependency_overrides[get_petdal] = lambda: pet_repo

    with TestClient(
        app=app,
        base_url="http://test/",
        headers={
            "X-API-Key": ApiSettings().api_key,
        },
    ) as test_client:
        yield test_client


def make_migrations(settings):
    config = alembic.config.Config()
    config.set_main_option("is_test", "True")
    config.set_main_option("script_location", "migrations")
    config.set_main_option("test_db_name", settings.name)
    alembic.command.upgrade(config, "head")


@pytest.fixture(scope="session")
def make_engine():
    settings = DatabaseSettings(name="databasefortest")
    create_database(settings.url)
    engine = create_engine(settings.url)
    make_migrations(settings)
    yield engine
    drop_database(settings.url)


@pytest.fixture(scope="function")
def create_session(make_engine):
    connection = make_engine.connect()
    transaction = connection.begin()
    session_maker = sessionmaker(bind=connection)
    session = session_maker()
    yield session
    session.close()
    transaction.rollback()
    connection.close()
