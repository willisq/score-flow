import { CompetitorRepository } from "#competitor/domain/repository/CompetitorRepository.js";

export class CompetitorDatabaseRepository extends CompetitorRepository {
	tableName = "competitor";

	async create(competitor, trx = null) {
		const competitorData = competitor.toJSON();

		const db = trx || this.databaseService;

		const [createdCompetitor] = await db(this.tableName)
			.insert(competitorData)
			.returning("*");

		return createdCompetitor;
	}
}