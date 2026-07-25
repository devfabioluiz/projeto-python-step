from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is not None:
        return _engine
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError(
            "DATABASE_URL não encontrada. "
            "Crie um banco no Supabase e coloque a URL no .env"
        )
    _engine = create_engine(DATABASE_URL)
    return _engine


class Base(DeclarativeBase):
    pass


def get_db():
    global _SessionLocal
    engine = get_engine()
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=engine)
        Base.metadata.create_all(bind=engine)
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()
