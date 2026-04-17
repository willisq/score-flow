from uuid import UUID
from typing import Optional

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.common.models import Base
from src.features.tournament.data.models import CategoryRegistrationModel, CategoryModalityModel


class RoundModel(Base):
    __tablename__ = "round"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    numero_participantes: Mapped[int] = mapped_column(Integer, nullable=False, default=2)


class MatchModel(Base):
    __tablename__ = "pyramid"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    round: Mapped[UUID] = mapped_column(ForeignKey("round.id"), nullable=False)
    first_competitor: Mapped[UUID] = mapped_column(ForeignKey("competitor_category.id"), nullable=False)
    second_competitor: Mapped[Optional[UUID]] = mapped_column(ForeignKey("competitor_category.id"), nullable=True)
    winner: Mapped[Optional[UUID]] = mapped_column(ForeignKey("competitor_category.id"), nullable=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    category_modality_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("category_modality.id"), nullable=True)

    round_rel: Mapped[RoundModel] = relationship()
    first_competitor_rel: Mapped[CategoryRegistrationModel] = relationship(foreign_keys=[first_competitor])
    second_competitor_rel: Mapped[Optional[CategoryRegistrationModel]] = relationship(foreign_keys=[second_competitor])
    winner_rel: Mapped[Optional[CategoryRegistrationModel]] = relationship(foreign_keys=[winner])
    category_modality_rel: Mapped[Optional[CategoryModalityModel]] = relationship()
