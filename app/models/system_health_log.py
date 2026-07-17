from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime
)

from datetime import datetime

from app.database.base import Base


class SystemHealthLog(Base):

    __tablename__ = "system_health_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    cpu_usage = Column(
        Float,
        nullable=False
    )

    memory_usage = Column(
        Float,
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
