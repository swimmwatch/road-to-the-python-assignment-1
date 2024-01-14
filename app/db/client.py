import contextlib

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .config import DatabaseSettings


@contextlib.contextmanager
def get_session():
    session = Session(
        bind=create_engine(DatabaseSettings().url), expire_on_commit=False
    )
    try:
        yield session
    except Exception as err:
        session.rollback()
        raise err
    finally:
        session.close()
