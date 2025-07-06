import { databaseService } from "#database/databaseService.js";

import { CategorySexDatabaseRepository } from "#category/infraestructure/CategorySexDatabaseRepository.js";
import { CategoryDatabaseRepository } from "#category/infraestructure/CategoryDatabaseRepository.js";

import { CreateCategoryWithSexes } from "#category/application/CreateCategoryWithSexes.js";

export class CategorySexController {
	static async create(req, res) {
		return databaseService.transaction(async (trx) => {
			const categoryRepository = new CategoryDatabaseRepository({
				databaseService: trx,
			});
			const categorySexRepository = new CategorySexDatabaseRepository({
				databaseService: trx,
			});

			const useCase = new CreateCategoryWithSexes({
				categoryRepository,
				categorySexRepository,
				databaseService,
			});

			const createdCategoryWithSexes = await useCase.execute(req.body);

			return res.status(201).json(createdCategoryWithSexes);
		});
	}
}
