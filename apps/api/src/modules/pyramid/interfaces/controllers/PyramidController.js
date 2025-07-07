import { databaseService } from "#database/databaseService.js";
import { UnitOfWork } from "#database/UnitOfWork.js";

import { AssemblePyramid } from "#pyramid/application/AssemblePyramid.js";

import { CompetitorDatabaseRepository } from "#competitor/infraestructure/CompetitorDatabaseRepository.js";
import { CategoryDatabaseRepository } from "#src/modules/category/infraestructure/CategoryDatabaseRepository.js";
import {PyramidDatabaseRepository} from "#pyramid/infraestructure/PyramidDatabaseRepository.js";

export class PyramidController {
	static async create(req, res) {
		const repositoriesClasses = {
			competitorRepository: CompetitorDatabaseRepository,
			categoryRepository: CategoryDatabaseRepository,
			pyramidRepository: PyramidDatabaseRepository
		};
		const unitOfWork = new UnitOfWork({ databaseService, repositoriesClasses });

		const useCase = new AssemblePyramid({ unitOfWork });

		const createdCompetitors = await useCase.execute(req.body);

		res.status(201).json(createdCompetitors);
	}
}
