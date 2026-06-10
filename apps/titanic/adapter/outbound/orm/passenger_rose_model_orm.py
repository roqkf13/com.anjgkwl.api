from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.grid_oracle_database import Base

class RoseModelOrm(Base):
    __tablename__ = "bookings"
    __table_args__ = (UniqueConstraint("person_id", name="uq_bookings_person_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    person_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("passenger.id"), nullable=True)
    pclass: Mapped[str | None] = mapped_column(String, nullable=True)
    ticket: Mapped[str | None] = mapped_column(String, nullable=True)
    fare: Mapped[str | None] = mapped_column(String, nullable=True)
    cabin: Mapped[str | None] = mapped_column(String, nullable=True)
    embarked: Mapped[str | None] = mapped_column(String, nullable=True)
