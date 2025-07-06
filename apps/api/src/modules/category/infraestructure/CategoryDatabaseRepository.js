import { CategoryRepository } from "#category/domain/repository/CategoryRepository.js";

export class CategoryDatabaseRepository extends CategoryRepository {
	tableName = "category";

	async create(category) {
		const categoryData = category.toJSON();

		const [createdCategory] = await this.databaseService(this.tableName)
			.insert(categoryData)
			.returning("*");

		return createdCategory;
	}
}
