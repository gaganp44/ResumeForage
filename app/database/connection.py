from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker,
)

from app.core.config import DATA_DIR


DATABASE_PATH = DATA_DIR / "resumeforge.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False
)


def initialize_database():
    from app.database import models

    Base.metadata.create_all(bind=engine)