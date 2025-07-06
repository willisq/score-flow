import { CategoryRankRepository } from "#category/domain/repository/CategoryRankRepository.js";

export class CategoryRankDatabaseRepository extends CategoryRankRepository {
	tableName = "category_rank";

	async create(categoryRanks) {
		const recordsToInsert = categoryRanks.map((categoryRank) =>
			categoryRank.toJSON(),
		);

		const [createdCategoryRank] = await this.databaseService(this.tableName)
			.insert(recordsToInsert)
			.returning("*");

		return createdCategoryRank;
	}
}
