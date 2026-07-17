from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from config import settings

engine = create_engine(
    url=settings.database_url,
    pool_size=20, # number of active connections allowed
    max_overflow=15, # additional connections when pool is full
    pool_timeout=30, # seconds to wait before returning error if no pool depleted
    pool_recycle=3600, # recreate connections to avoid stale connections
    echo=False, # Disable production logging
)

class Base(DeclarativeBase):
    pass

SessionLocal = Session(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()