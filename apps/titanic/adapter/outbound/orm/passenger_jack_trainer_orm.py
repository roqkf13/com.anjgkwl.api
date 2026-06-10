from __future__ import annotations

from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.grid_oracle_database import Base

class JackTrainerOrm(Base):
    __tablename__ = "passenger"
    __table_args__ = (UniqueConstraint("passenger_id", name="uq_passenger_passenger_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    passenger_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    survived: Mapped[int | None] = mapped_column(Integer, nullable=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    gender: Mapped[str | None] = mapped_column(String, nullable=True)
    age: Mapped[str | None] = mapped_column(String, nullable=True)
    sib_sp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    parch: Mapped[int | None] = mapped_column(Integer, nullable=True)

TitanicRecord = JackTrainerOrm
