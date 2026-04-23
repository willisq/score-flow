import math
from typing import List, Dict, Optional
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.features.bracket.domain.entities import Match, Round
from src.features.bracket.data.models import MatchModel, RoundModel
from src.features.registration.data.models import CompetitorModel, AcademyModel, RankModel
from src.features.tournament.data.models import (
    CategoryRegistrationModel, 
    CategoryModalityModel, 
    CategoryModel, 
    RankGroupModel, 
    PhysicalRequirementModel
)

class RoundRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_initial_round(self, num_competitors: int) -> Round:
        # Calcular los participantes máximos (potencia de 2 más cercana)
        needed_slots = 2 ** math.ceil(math.log2(num_competitors)) if num_competitors > 1 else 2
        
        stmt = select(RoundModel).where(RoundModel.numero_participantes == needed_slots)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            # Si no conseguimos la ronda exacta configurada en db, buscamos la de mayor cercanía o disparamos error
            raise ValueError(f"No se encontró una configuración de Ronda para {needed_slots} participantes en la Base de Datos.")
            
        return Round(
            id=model.id,
            description=model.description,
            sequence=1 # Por el momento el domain impone una secuencia que la bd no trackea.
        )


class BracketRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def clear_category_modality_brackets(self, category_modality_ids: List[UUID]) -> None:
        """Elimina todos los brackets existentes de las category-modalities especificadas."""
        if not category_modality_ids:
            return
            
        stmt = delete(MatchModel).where(MatchModel.category_modality_id.in_(category_modality_ids))
        await self.session.execute(stmt)

    async def save_matches(self, category_modality_id: UUID, matches: List[Match], registration_map: Dict[UUID, UUID]) -> None:
        """
        Guarda los emparejamientos en la Base de Datos.
        `registration_map` es un diccionario `{competitor_id: category_registration_id}`
        para poder satisfacer las Foreign Keys de la tabla pyramid.
        """
        models_to_insert = []
    
        for match in matches:
            # Mapeamos los Competitors de Dominio (cuyos id son competitor_id) al category_registration_id que exige la BD
            first_reg_id = registration_map.get(match.first_competitor.id) if match.first_competitor else None
            second_reg_id = registration_map.get(match.second_competitor.id) if match.second_competitor else None
            winner_reg_id = registration_map.get(match.winner.id) if match.winner else None
            
            if not first_reg_id:
                raise ValueError(f"Primer competidor en match {match.id} no posee Inscription Activa en la categoría")

            model = MatchModel(
                id=match.id,
                round=match.round.id,
                first_competitor=first_reg_id,
                second_competitor=second_reg_id,
                winner=winner_reg_id,
                position=match.position,
                category_modality_id=category_modality_id
            )
            models_to_insert.append(model)
            
            
        self.session.add_all(models_to_insert)

    async def get_matches(
        self, 
        categories: Optional[List[UUID]] = None, 
        rounds: Optional[List[UUID]] = None,
        rank_id: Optional[UUID] = None,
        age: Optional[int] = None,
        modality_id: Optional[UUID] = None,
        special_condition: Optional[bool] = None,
        weight: Optional[float] = None
    ) -> List[MatchModel]:
        stmt = (
            select(MatchModel)
            .options(
                selectinload(MatchModel.round_rel),
                selectinload(MatchModel.first_competitor_rel)
                    .selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.person),
                selectinload(MatchModel.first_competitor_rel)
                    .selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.academy).selectinload(AcademyModel.instructor),
                selectinload(MatchModel.first_competitor_rel)
                    .selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.rank),
                selectinload(MatchModel.first_competitor_rel)
                    .selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.sex),
                
                selectinload(MatchModel.second_competitor_rel)
                    .selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.person),
                selectinload(MatchModel.second_competitor_rel)
                    .selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.academy).selectinload(AcademyModel.instructor),
                selectinload(MatchModel.second_competitor_rel)
                    .selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.rank),
                selectinload(MatchModel.second_competitor_rel)
                    .selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.sex),
                
                selectinload(MatchModel.winner_rel)
                    .selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.person),
                selectinload(MatchModel.winner_rel)
                    .selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.academy).selectinload(AcademyModel.instructor),
                selectinload(MatchModel.winner_rel)
                    .selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.rank),
                selectinload(MatchModel.winner_rel)
                    .selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.sex),
            )
        )
        
        # Determine if we need to join CategoryModality
        needs_category_modality_join = any(x is not None for x in [rank_id, age, modality_id, special_condition, weight])
        
        if needs_category_modality_join:
            stmt = stmt.join(MatchModel.category_modality_rel)
            
        if categories:
            stmt = stmt.where(MatchModel.category_modality_id.in_(categories))
        if rounds:
            stmt = stmt.where(MatchModel.round.in_(rounds))
            
        if modality_id:
            stmt = stmt.where(CategoryModalityModel.modality_id == modality_id)
            
        if rank_id:
            stmt = stmt.join(CategoryModalityModel.rank_group).join(RankGroupModel.ranks)
            stmt = stmt.where(RankModel.id == rank_id)
            
        if weight is not None:
            stmt = stmt.join(CategoryModalityModel.physical_requirement)
            stmt = stmt.where(PhysicalRequirementModel.initial_weight <= weight)
            stmt = stmt.where(PhysicalRequirementModel.final_weight >= weight)
            
        if age is not None or special_condition is not None:
            # We must join CategoryModel exactly once if age or special_condition is present
            stmt = stmt.join(CategoryModalityModel.category)
            if age is not None:
                stmt = stmt.where(CategoryModel.ages.contains([age]))
            if special_condition is not None:
                stmt = stmt.where(CategoryModel.special_condition == special_condition)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
