from typing import List
from uuid import uuid4

from src.features.registration.domain.entities import Competitor
from src.features.tournament.domain.entities import (
    Category,
    CategoryRegistration,
    Tournament,
)


class AutoRegistrationService:
    """
    Domain service responsible for evaluating a list of competitors against
    a list of categories and automatically creating their CategoryRegistration entities.
    """

    @staticmethod
    def auto_register_competitors(
        competitors: List[Competitor],
        categories: List[Category],
        tournament: Tournament,
    ) -> List[CategoryRegistration]:
        """
        Classifies competitors based on mathematical conditions and returns
        CategoryRegistration entities ready for persistence.
        """
        registrations: List[CategoryRegistration] = []

        for competitor in competitors:
            for category in categories:
                if category.is_eligible(competitor):
                    new_registration = CategoryRegistration(
                        id=uuid4(),
                        competitor=competitor,
                        category=category,
                        tournament=tournament,
                    )
                    registrations.append(new_registration)

        return registrations
