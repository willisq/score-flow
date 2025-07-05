import { RoundRepository } from "#round/domain/repositories/RoundRepository.js";

export class RoundDatabaseRepository extends RoundRepository {
	tableName = "round";

	async create(round, trx = null) {
		const roundData = round.toJSON();
		const db = trx || this.databaseService;

		const [createdRound] = await db(this.tableName)
			.insert(roundData)
			.returning("*");

		return createdRound;
	}

	async findAll(trx = null) {
		const db = trx || this.databaseService;
		return db(this.tableName).select("*").orderBy("created_at", "asc");
	}

	async findById(id, trx = null) {
		const db = trx || this.databaseService;
		return db(this.tableName).where({ id }).first();
	}
}