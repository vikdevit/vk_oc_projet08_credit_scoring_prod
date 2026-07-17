from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime
)

from datetime import datetime

from app.database.base import Base


class ApiLog(Base):

    __tablename__ = "api_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    endpoint = Column(
        String(100),
        nullable=False
    )

    status_code = Column(
        Integer,
        nullable=False
    )

    response_time = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
