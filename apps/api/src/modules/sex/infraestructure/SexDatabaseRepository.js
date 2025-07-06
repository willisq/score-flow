import { SexRepository } from "#sex/domain/repositories/SexRepository.js";

export class SexDatabaseRepository extends SexRepository {
	tableName = "sex";

	async create(sex, trx = null) {
		const sexData = sex.toJSON();
		const db = trx || this.databaseService;

		const [createdSex] = await db(this.tableName)
			.insert(sexData)
			.returning("*");

		return createdSex;
	}

	async findAll(trx = null) {
		const db = trx || this.databaseService;
		return db(this.tableName).select("*").orderBy("abbreviation", "asc");
	}
}