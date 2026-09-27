from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class RiskProfile(Base):
    __tablename__ = "risk_profiles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    sex: Mapped[int] = mapped_column(
        nullable=False
    )

    general_health: Mapped[int] = mapped_column(
        nullable=False
    )

    physical_health_days: Mapped[int] = mapped_column(
        nullable=False
    )

    physical_activity: Mapped[int] = mapped_column(
        nullable=False
    )

    smoking: Mapped[int] = mapped_column(
        nullable=False
    )

    alcohol: Mapped[int] = mapped_column(
        nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="risk_profile"
    )
    