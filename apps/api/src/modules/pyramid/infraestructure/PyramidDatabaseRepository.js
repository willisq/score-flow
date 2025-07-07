import { PyramidRepository } from "#pyramid/domain/repositories/PyramidRepository.js";

export class PyramidDatabaseRepository extends PyramidRepository {
	tableName = "pyramid";

	async createBulk(matches) {
		const dataToInsert = matches.map((match) => ({
			id: match.id,
			first_competitor: match.firstCompetitor,
			second_competitor: match.secondCompetitor,
			round: this.databaseService("round")
				.select("id")
				.where("description", match.roundName),
		}));

		if (dataToInsert.length === 0) return [];

		return this.databaseService(this.tableName)
			.insert(dataToInsert)
			.returning("*");
	}

	async deleteAllPyramids() {
		return this.databaseService(this.tableName).del();
	}
}
