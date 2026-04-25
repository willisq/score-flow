from datetime import datetime
from uuid import UUID
from typing import List, Optional

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Table, Column, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from src.core.common.models import Base
from src.features.registration.data.models import RankModel, SexModel, CompetitorModel


# Association tables for Category/Rank relationships
rank_group_item = Table(
    "rank_group_item",
    Base.metadata,
    Column("rank_group_id", ForeignKey("rank_group.id", ondelete="CASCADE"), primary_key=True),
    Column("rank_id", ForeignKey("rank.id", ondelete="CASCADE"), primary_key=True),
)

category_modality_sex = Table(
    "category_modality_sex",
    Base.metadata,
    Column("category_modality_id", ForeignKey("category_modality.id"), primary_key=True),
    Column("sex_id", ForeignKey("sex.id"), primary_key=True),
)


class ModalityModel(Base):
    __tablename__ = "modality"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


class RankGroupModel(Base):
    __tablename__ = "rank_group"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    ranks: Mapped[List[RankModel]] = relationship(secondary=rank_group_item)


class TournamentModel(Base):
    __tablename__ = "tournament"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    registrations: Mapped[List["CategoryRegistrationModel"]] = relationship(
        back_populates="tournament"
    )


class PhysicalRequirementModel(Base):
    __tablename__ = "physical_requirement"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    initial_weight: Mapped[float] = mapped_column(Float, nullable=True)
    final_weight: Mapped[float] = mapped_column(Float, nullable=True)
    initial_height: Mapped[float] = mapped_column(Float, nullable=True)
    final_height: Mapped[float] = mapped_column(Float, nullable=True)


class CategoryModel(Base):
    __tablename__ = "category"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    ages: Mapped[List[int]] = mapped_column(ARRAY(Integer), nullable=False)
    special_condition: Mapped[bool] = mapped_column(Boolean, default=False)

    modalities: Mapped[List["CategoryModalityModel"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )


class CategoryModalityModel(Base):
    __tablename__ = "category_modality"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    category_id: Mapped[UUID] = mapped_column(ForeignKey("category.id"), nullable=False)
    modality_id: Mapped[UUID] = mapped_column(ForeignKey("modality.id"), nullable=False)
    rank_group_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("rank_group.id"), nullable=True)
    physical_requirement_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("physical_requirement.id"), nullable=True
    )

    category: Mapped[CategoryModel] = relationship(back_populates="modalities")
    sexes: Mapped[List[SexModel]] = relationship(secondary=category_modality_sex)
    modality: Mapped[ModalityModel] = relationship()
    rank_group: Mapped[Optional[RankGroupModel]] = relationship()
    physical_requirement: Mapped[Optional[PhysicalRequirementModel]] = relationship()
    registrations: Mapped[List["CategoryRegistrationModel"]] = relationship(
        back_populates="category_modality"
    )


class CategoryRegistrationModel(Base):
    __tablename__ = "competitor_category"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    competitor_id: Mapped[UUID] = mapped_column(
        ForeignKey("competitor.id"), nullable=False
    )
    category_modality_id: Mapped[UUID] = mapped_column(
        ForeignKey("category_modality.id"), nullable=False
    )
    tournament_id: Mapped[UUID] = mapped_column(
        ForeignKey("tournament.id"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    competitor: Mapped[CompetitorModel] = relationship()
    category_modality: Mapped[CategoryModalityModel] = relationship(
        back_populates="registrations"
    )
    tournament: Mapped[TournamentModel] = relationship(back_populates="registrations")
