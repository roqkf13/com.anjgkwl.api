from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TitanicRecord(Base):
    __tablename__ = "titanic_passengers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    passenger_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    survived: Mapped[str | None] = mapped_column(String(8), nullable=True)
    pclass: Mapped[str | None] = mapped_column(String(8), nullable=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(16), nullable=True)
    age: Mapped[str | None] = mapped_column(String(16), nullable=True)
    sib_sp: Mapped[str | None] = mapped_column(String(8), nullable=True)
    parch: Mapped[str | None] = mapped_column(String(8), nullable=True)
    ticket: Mapped[str | None] = mapped_column(String(64), nullable=True)
    fare: Mapped[str | None] = mapped_column(String(32), nullable=True)
    cabin: Mapped[str | None] = mapped_column(String(64), nullable=True)
    embarked: Mapped[str | None] = mapped_column(String(8), nullable=True)
