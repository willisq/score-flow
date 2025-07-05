import { RankRepository } from "#rank/domain/repositories/RankRepository.js";

export class RankDatabaseRepository extends RankRepository {
	tableName = "rank";

	async create(rank, trx = null) {
		const rankData = rank.toJSON();
		const db = trx || this.databaseService;

		const [createdRank] = await db(this.tableName)
			.insert(rankData)
			.returning("*");

		return createdRank;
	}

	async findAll(trx = null) {
		const db = trx || this.databaseService;
		return db(this.tableName).select("*").orderBy("classification", "asc");
	}

	async findById(id, trx = null) {
		const db = trx || this.databaseService;
		return db(this.tableName).where({ id }).first();
	}
}