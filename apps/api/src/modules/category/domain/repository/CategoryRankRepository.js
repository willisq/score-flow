export class CategoryRankRepository {
	constructor({ databaseService }) {
		this.databaseService = databaseService;
	}

	async create(category, rank) {
		throw new Error("Método create no implementado");
	}
}
