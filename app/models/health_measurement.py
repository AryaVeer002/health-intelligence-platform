from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class HealthMeasurement(Base):
    __tablename__ = "health_measurements"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    report_id: Mapped[int | None] = mapped_column(
        ForeignKey("reports.id"),
        nullable=True
    )

    metric: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    value: Mapped[float] = mapped_column(
        nullable=False
    )

    unit: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    measured_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )   