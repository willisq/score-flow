import { CategorySexRepository } from "#category/domain/repository/CategorySexRepository.js";

export class CategorySexDatabaseRepository extends CategorySexRepository {
	tableName = "category_sex";

	async createCategoryWithSexes(categorySexes, trx = null) {
		const db = trx || this.databaseService;

		const recordsToInsert = categorySexes.map((categorySex) =>
			categorySex.toJSON(),
		);

		const createdRecords = await db(this.tableName)
			.insert(recordsToInsert)
			.returning("*");

		return createdRecords;
	}
}
