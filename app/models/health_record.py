from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class HealthRecord(Base):
    __tablename__ = "health_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    record_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    weight: Mapped[float] = mapped_column(nullable=False)

    height: Mapped[float] = mapped_column(nullable=False)

    heart_rate: Mapped[int] = mapped_column(nullable=False)