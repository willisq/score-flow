import { CompetitorRepository } from "#competitor/domain/repository/CompetitorRepository.js";
import { CompetitorCategory } from "../domain/entities/CompetitorCategory.js";

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


	/**
	 * Finds all competitor-category entries for a given championship.
	 * @param {string} championshipId - The UUID of the championship.
	 * @returns {Promise<CompetitorCategory[]>} A list of CompetitorCategory entity instances.
	 */
	async findAllByChampionship(championshipId) {		
		const records = await this.databaseService("competitor_category")
			.where({ championship: championshipId })
			.select("*");

		return records.map((record) => new CompetitorCategory(record));
	}
}
