from uuid import UUID

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.common.models import Base


class SexModel(Base):
    __tablename__ = "sex"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class PersonModel(Base):
    __tablename__ = "person"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    academies_instructed: Mapped[list["AcademyModel"]] = relationship(
        back_populates="instructor",
    )
    competitor: Mapped["CompetitorModel"] = relationship(
        back_populates="person",
        uselist=False,
    )


class RankModel(Base):
    __tablename__ = "rank"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    classification: Mapped[int] = mapped_column(Integer, nullable=False)
    is_black_belt: Mapped[bool] = mapped_column(Boolean, default=False)


class AcademyModel(Base):
    __tablename__ = "academy"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    instructor_id: Mapped[UUID] = mapped_column(ForeignKey("person.id"), nullable=False)

    instructor: Mapped[PersonModel] = relationship(
        back_populates="academies_instructed"
    )
    competitors: Mapped[list["CompetitorModel"]] = relationship(
        back_populates="academy"
    )


class CompetitorModel(Base):
    __tablename__ = "competitor"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    person_id: Mapped[UUID] = mapped_column(ForeignKey("person.id"), nullable=False)
    academy_id: Mapped[UUID] = mapped_column(ForeignKey("academy.id"), nullable=False)
    rank_id: Mapped[UUID] = mapped_column(ForeignKey("rank.id"), nullable=False)
    sex_id: Mapped[UUID] = mapped_column(ForeignKey("sex.id"), nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    special_condition: Mapped[bool] = mapped_column(Boolean, default=False)

    person: Mapped[PersonModel] = relationship(back_populates="competitor")
    academy: Mapped[AcademyModel] = relationship(back_populates="competitors")
    rank: Mapped[RankModel] = relationship()
    sex: Mapped[SexModel] = relationship()
