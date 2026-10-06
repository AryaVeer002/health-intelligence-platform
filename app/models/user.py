from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    is_deleted: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    health_profile: Mapped["HealthProfile | None"] = relationship(
        back_populates="user",
        uselist=False
    )

    risk_profile: Mapped["RiskProfile | None"] = relationship(
        back_populates="user",
        uselist=False
    )