from uuid import UUID
from typing import List

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from src.core.common.models import Base
from src.features.registration.data.models import RankModel, SexModel, CompetitorModel


# Association tables for Category many-to-many relationships
category_rank = Table(
    "category_rank",
    Base.metadata,
    Column("category_id", ForeignKey("category.id"), primary_key=True),
    Column("rank_id", ForeignKey("rank.id"), primary_key=True),
)

category_sex = Table(
    "category_sex",
    Base.metadata,
    Column("category_id", ForeignKey("category.id"), primary_key=True),
    Column("sex_id", ForeignKey("sex.id"), primary_key=True),
)


class ModalityModel(Base):
    __tablename__ = "modality"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    categories: Mapped[List["CategoryModel"]] = relationship(back_populates="modality")


class TournamentModel(Base):
    __tablename__ = "tournament"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    registrations: Mapped[List["CategoryRegistrationModel"]] = relationship(
        back_populates="tournament"
    )


class CategoryModel(Base):
    __tablename__ = "category"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    ages: Mapped[List[int]] = mapped_column(ARRAY(Integer), nullable=False)
    special_condition: Mapped[bool] = mapped_column(Boolean, default=False)
    modality_id: Mapped[UUID] = mapped_column(ForeignKey("modality.id"), nullable=False)
    initial_weight: Mapped[float] = mapped_column(Float, nullable=True)
    final_weight: Mapped[float] = mapped_column(Float, nullable=True)
    initial_height: Mapped[float] = mapped_column(Float, nullable=True)
    final_height: Mapped[float] = mapped_column(Float, nullable=True)

    modality: Mapped[ModalityModel] = relationship(back_populates="categories")
    ranks: Mapped[List[RankModel]] = relationship(secondary=category_rank)
    sexes: Mapped[List[SexModel]] = relationship(secondary=category_sex)
    registrations: Mapped[List["CategoryRegistrationModel"]] = relationship(
        back_populates="category"
    )


class CategoryRegistrationModel(Base):
    __tablename__ = "competitor_category"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    competitor_id: Mapped[UUID] = mapped_column(
        ForeignKey("competitor.id"), nullable=False
    )
    category_id: Mapped[UUID] = mapped_column(ForeignKey("category.id"), nullable=False)
    tournament_id: Mapped[UUID] = mapped_column(
        ForeignKey("tournament.id"), nullable=False
    )

    competitor: Mapped[CompetitorModel] = relationship()
    category: Mapped[CategoryModel] = relationship(back_populates="registrations")
    tournament: Mapped[TournamentModel] = relationship(back_populates="registrations")
