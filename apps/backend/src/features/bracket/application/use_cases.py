import uuid
from uuid import UUID
from typing import List, Optional
from collections import defaultdict

from src.features.bracket.application.schemas import GenerateBracketsRequest, GeneratedCategoryResult, MatchSchema, RoundSchema
from src.features.registration.application.schemas import CompetitorSchema, AcademySchema, PersonSchema, RankSchema, SexSchema
from src.features.bracket.data.repository import BracketRepository, RoundRepository
from src.features.tournament.data.repository import CategoryRegistrationRepository
from src.features.bracket.domain.entities import Pyramid
from src.features.bracket.domain.pairing_strategies import AcademyAwarePairingStrategy


class BracketUseCases:
    def __init__(
        self,
        bracket_repo: BracketRepository,
        round_repo: RoundRepository,
        registration_repo: CategoryRegistrationRepository
    ):
        self.bracket_repo = bracket_repo
        self.round_repo = round_repo
        self.registration_repo = registration_repo

    async def generate_initial_brackets(self, request: GenerateBracketsRequest) -> List[GeneratedCategoryResult]:
        # 1. Obtener inscripciones
        registrations = await self.registration_repo.get_by_categories(request.category_modality_ids)
        if not registrations:
            return []

        # 2. Agrupar por category_modality
        grouped_competitors = defaultdict(list)
        grouped_category_entities = {}
        registration_maps = defaultdict(dict)

        for reg in registrations:
            cm_id = reg.category_modality.id
            comp_id = reg.competitor.id
            
            grouped_competitors[cm_id].append(reg.competitor)
            grouped_category_entities[cm_id] = reg.category_modality.category
            
            # Map para Foreign Keys de la base de datos (competitor.id -> category_registration.id)
            registration_maps[cm_id][comp_id] = reg.id

        # 3. Limpiar las pirámides previas para las category_modalities detectadas
        actual_cm_ids = list(grouped_competitors.keys())
        await self.bracket_repo.clear_category_modality_brackets(actual_cm_ids)

        # 4. Generar pares y guardar en base de datos
        pairing_strategy = AcademyAwarePairingStrategy()
        results = []

        for cm_id, competitors in grouped_competitors.items():
            num_competitors = len(competitors)
            if num_competitors == 0:
                continue

            first_round = await self.round_repo.get_initial_round(num_competitors)
            category = grouped_category_entities[cm_id]
            pyramid = Pyramid(id=uuid.uuid4(), category=category)
            
            matches = pyramid.generate_initial_round(
                competitors=competitors,
                first_round=first_round,
                pairing_strategy=pairing_strategy
            )
            
            # Auto-advance the BYEs to the next round structure
            next_round = await self.round_repo.get_next_round(first_round)
            new_matches = []
            if next_round:
                new_matches = pyramid.advance(
                    current_round=first_round,
                    next_round=next_round,
                    require_complete=False
                )
            
            await self.bracket_repo.save_matches(cm_id, matches + new_matches, registration_maps[cm_id])
            results.append(GeneratedCategoryResult(category_modality_id=cm_id, matches_generated=len(matches)))

        return results

    async def get_brackets(
        self, 
        categories: Optional[List[UUID]] = None, 
        rounds: Optional[List[UUID]] = None,
        rank_id: Optional[UUID] = None,
        age: Optional[int] = None,
        modality_id: Optional[UUID] = None,
        special_condition: Optional[bool] = None,
        weight: Optional[float] = None,
        sex_id: Optional[UUID] = None,
    ) -> List[MatchSchema]:
        models = await self.bracket_repo.get_matches(
            categories=categories, 
            rounds=rounds,
            rank_id=rank_id,
            age=age,
            modality_id=modality_id,
            special_condition=special_condition,
            weight=weight,
            sex_id=sex_id
        )
        
        def map_competitor(reg_model) -> Optional[CompetitorSchema]:
            if not reg_model or not reg_model.competitor:
                return None
            c = reg_model.competitor
            return CompetitorSchema(
                id=c.id,
                first_name=c.person.first_name,
                last_name=c.person.last_name,
                academy=AcademySchema(
                    id=c.academy.id, 
                    name=c.academy.name, 
                    instructor=PersonSchema(
                        id=c.academy.instructor.id, 
                        first_name=c.academy.instructor.first_name, 
                        last_name=c.academy.instructor.last_name
                    )
                ),
                rank=RankSchema(
                    id=c.rank.id, 
                    name=c.rank.name, 
                    classification=c.rank.classification, 
                    is_black_belt=c.rank.is_black_belt
                ),
                sex=SexSchema(id=c.sex.id, name=c.sex.name),
                weight=c.weight,
                height=c.height,
                age=c.age,
                special_condition=c.special_condition,
                registration_id=reg_model.id
            )
            
        matches = []
        for m in models:
            matches.append(MatchSchema(
                id=m.id,
                round=RoundSchema(id=m.round_rel.id, description=m.round_rel.description),
                position=m.position,
                category_modality_id=m.category_modality_id,
                first_competitor=map_competitor(m.first_competitor_rel),
                second_competitor=map_competitor(m.second_competitor_rel),
                winner=map_competitor(m.winner_rel)
            ))
            
        return matches

    async def delete_pyramid(self, category_modality_id: UUID) -> None:
        await self.bracket_repo.clear_category_modality_brackets([category_modality_id])

    async def remove_competitor_and_recalculate(
        self, 
        category_modality_id: UUID, 
        registration_id: UUID,
        remove_from_category: bool = False
    ) -> List[GeneratedCategoryResult]:
        # 1. Limpiar los brackets primero para evitar violaciones de FK
        await self.bracket_repo.clear_category_modality_brackets([category_modality_id])
        await self.bracket_repo.session.flush()

        # 2. Manejar la inscripción según la bandera
        if remove_from_category:
            success = await self.registration_repo.delete_registration(registration_id)
        else:
            # Solo se quita de la pirámide (desactivar)
            success = await self.registration_repo.deactivate_registration(registration_id)

        if not success:
            raise ValueError(f"No se encontró la inscripción {registration_id}")
        
        await self.bracket_repo.session.flush()
            
        # 3. Regenerar la pirámide
        return await self.generate_initial_brackets(
            GenerateBracketsRequest(category_modality_ids=[category_modality_id])
        )
