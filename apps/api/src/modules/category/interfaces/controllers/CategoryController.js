import { databaseService } from "#database/databaseService.js";
import { UnitOfWork } from "#database/UnitOfWork.js";

import { CreateBulkCategories } from "#category/application/CreateCategory.js";

import { CategoryDatabaseRepository } from "#category/infraestructure/CategoryDatabaseRepository.js";
import { CategorySexDatabaseRepository } from "#category/infraestructure/CategorySexDatabaseRepository.js";
import { CategoryRankDatabaseRepository } from "#category/infraestructure/CategoryRankDatabaseRepository.js";

export class CategoryController {
	static async create(req, res) {
		const repositoriesClasses = {
			categoryRepository: CategoryDatabaseRepository,
			categorySexRepository: CategorySexDatabaseRepository,
			categoryRankRepository: CategoryRankDatabaseRepository,
		};
		const unitOfWork = new UnitOfWork({
			databaseService,
			repositoriesClasses,
		});

		const useCase = new CreateBulkCategories({ unitOfWork });
		
		const createdCategories = await useCase.execute(req.body);

		return res.status(201).json(createdCategories);
	}
}
