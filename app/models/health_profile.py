from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class HealthProfile(Base):
    __tablename__ = "health_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    age: Mapped[int] = mapped_column(nullable=False)

    weight: Mapped[float] = mapped_column(nullable=False)

    height: Mapped[float] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(
        back_populates="health_profile"
    )