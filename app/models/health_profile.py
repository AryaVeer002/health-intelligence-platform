from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class HealthProfile(Base):
    __tablename__ = "health_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    age: Mapped[int] = mapped_column(nullable=False)

    weight: Mapped[float] = mapped_column(nullable=False)

    height: Mapped[float] = mapped_column(nullable=False)