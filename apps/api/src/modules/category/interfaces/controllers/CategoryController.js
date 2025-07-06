import { databaseService } from "#src/services/database/databaseService.js";
import { CreateCategory } from "#category/application/CreateCategory.js";
import { CategoryDatabaseRepository } from "#category/infraestructure/CategoryDatabaseRepository.js";

export class CategoryController {
	static async create(req, res) {
		return databaseService.transaction(async (trx) => {
			const useCase = new CreateCategory({
				categoryRepository: new CategoryDatabaseRepository({
					databaseService: trx,
				}),
			});

			const createdCategory = await useCase.execute(req.body);

			return res.status(201).json(createdCategory);
		});
	}
}
