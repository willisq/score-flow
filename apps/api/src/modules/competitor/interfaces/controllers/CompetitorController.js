import { databaseService } from "#database/databaseService.js";
import { UnitOfWork } from "#database/UnitOfWork.js";

import { CreateBulkCompetitors } from "#competitor/application/CreateCompetitor.js";
import {FindCompetitorsByCategory} from "#competitor/application/FindCompetitorsByCategory.js";

import { CompetitorDatabaseRepository } from "#competitor/infraestructure/CompetitorDatabaseRepository.js";
import { CategoryDatabaseRepository } from "#src/modules/category/infraestructure/CategoryDatabaseRepository.js";
import { PersonDatabaseRepository } from "#person/infraestructure/PersonDatabaseRepository.js";
export class CompetitorController {
	static async create(req, res) {
		const repositoriesClasses = {
			personRepository: PersonDatabaseRepository,
			competitorRepository: CompetitorDatabaseRepository,
			categoryRepository: CategoryDatabaseRepository,
		};
		const unitOfWork = new UnitOfWork({ databaseService, repositoriesClasses });

		const useCase = new CreateBulkCompetitors({ unitOfWork });

		const createdCompetitors = await useCase.execute(req.body);

		res.status(201).json(createdCompetitors);
	}

	static async findByCategory(req, res, next) {
		const { category, championship } = req.query;

		const competitorRepository = new CompetitorDatabaseRepository({
			databaseService,
		});
		const useCase = new FindCompetitorsByCategory({ competitorRepository });

		const competitors = await useCase.execute({ category, championship });

		return res.status(200).json(competitors);
	}
}
