from dotenv import load_dotenv
import os

from sqlalchemy import create_engine


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)
