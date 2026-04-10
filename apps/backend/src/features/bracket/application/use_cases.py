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
        registrations = await self.registration_repo.get_by_categories(request.categories)
        if not registrations:
            return []

        # 2. Agrupar por categoría
        grouped_competitors = defaultdict(list)
        grouped_category_entities = {}
        registration_maps = defaultdict(dict)

        for reg in registrations:
            cat_id = reg.category.id
            comp_id = reg.competitor.id
            
            grouped_competitors[cat_id].append(reg.competitor)
            grouped_category_entities[cat_id] = reg.category
            
            # Map para Foreign Keys de la base de datos (competitor.id -> category_registration.id)
            registration_maps[cat_id][comp_id] = reg.id

        # 3. Limpiar las pirámides previas para las categorías detectadas
        actual_category_ids = list(grouped_competitors.keys())
        await self.bracket_repo.clear_category_brackets(actual_category_ids)

        # 4. Generar pares y guardar en base de datos
        pairing_strategy = AcademyAwarePairingStrategy()
        results = []

        for cat_id, competitors in grouped_competitors.items():
            num_competitors = len(competitors)
            if num_competitors == 0:
                continue

            first_round = await self.round_repo.get_initial_round(num_competitors)
            category = grouped_category_entities[cat_id]
            pyramid = Pyramid(id=uuid.uuid4(), category=category)
            
            matches = pyramid.generate_initial_round(
                competitors=competitors,
                first_round=first_round,
                pairing_strategy=pairing_strategy
            )
            
            await self.bracket_repo.save_matches(cat_id, matches, registration_maps[cat_id])
            results.append(GeneratedCategoryResult(category_id=cat_id, matches_generated=len(matches)))

        return results

    async def get_brackets(self, categories: Optional[List[UUID]] = None, rounds: Optional[List[UUID]] = None) -> List[MatchSchema]:
        models = await self.bracket_repo.get_matches(categories, rounds)
        
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
                special_condition=c.special_condition
            )
            
        matches = []
        for m in models:
            matches.append(MatchSchema(
                id=m.id,
                round=RoundSchema(id=m.round_rel.id, description=m.round_rel.description),
                position=m.position,
                category_id=m.category_id,
                first_competitor=map_competitor(m.first_competitor_rel),
                second_competitor=map_competitor(m.second_competitor_rel),
                winner=map_competitor(m.winner_rel)
            ))
            
        return matches
