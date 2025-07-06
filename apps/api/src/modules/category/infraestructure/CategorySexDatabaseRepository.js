import { CategorySexRepository } from "#category/domain/repository/CategorySexRepository.js";

export class CategorySexDatabaseRepository extends CategorySexRepository {
	tableName = "category_sex";

	async create(categorySexes) {

		const recordsToInsert = categorySexes.map((categorySex) =>
			categorySex.toJSON(),
		);

		const createdRecords = await this.databaseService(this.tableName)
			.insert(recordsToInsert)
			.returning("*");

		return createdRecords;
	}
}
