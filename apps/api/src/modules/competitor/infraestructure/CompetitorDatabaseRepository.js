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

	async findCompetitorsByCategory(categoryId, championshipId) {
		const competitorsData = await this.databaseService(
			"competitor_category as cc",
		)
			.select(
				"c.id",
				"c.weight",
				"c.height",
				"c.age",
				"c.special_condition",
				"c.academy",
				this.databaseService.raw(
					"json_build_object('id', p.id, 'firstname', p.firstname, 'lastname', p.lastname) as person",
				),
				this.databaseService.raw(
					"json_build_object('id', r.id, 'description', r.description) as rank",
				),
				this.databaseService.raw(
					"json_build_object('id', s.id, 'description', s.description) as sex",
				),
			)
			.leftJoin("competitor as c", "c.id", "cc.competitor")
			.leftJoin("person as p", "p.id", "c.student")
			.leftJoin("rank as r", "r.id", "c.rank")
			.leftJoin("sex as s", "s.id", "c.sex")
			.where({
				"cc.category": categoryId,
				"cc.championship": championshipId,
			});

		return competitorsData;
	}
}
