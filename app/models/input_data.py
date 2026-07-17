from sqlalchemy import Column, Integer, DateTime, JSON
from datetime import datetime

from app.database.base import Base


class InputData(Base):

    __tablename__ = "input_data"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    client_id = Column(
        Integer,
        nullable=False
    )

    features = Column(
        JSON,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
