import os

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(
    DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://"
    )
)


def load_table(table_name):
    """
    Charge une table PostgreSQL depuis Neon
    """

    query = f"""
    SELECT *
    FROM {table_name};
    """

    return pd.read_sql(
        query,
        engine
    )


def load_predictions():
    return load_table("predictions")


def load_api_logs():
    return load_table("api_logs")


def load_system_health_logs():
    return load_table("system_health_logs")


def load_input_data():
    return load_table("input_data")


def load_reference_stats():
    return load_table("reference_stats")
