from sqlalchemy.orm import sessionmaker

from app.database.connection import engine

if engine:

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )


def get_db():

    if not engine:
        raise Exception(
            "Database not configured"
        )

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
