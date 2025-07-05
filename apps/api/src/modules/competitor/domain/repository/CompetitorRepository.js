export class CompetitorRepository {
	constructor({ databaseService }) {
		this.databaseService = databaseService;
	}

	async create(competitor, trx) {
		throw new Error("Método create no implementado");
	}
}
