from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import Generator

from crud_backend.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session() -> Generator[Session, None, None]:  # pragma: no cover
    with Session(engine) as session:
        yield session
