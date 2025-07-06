export class CategoryRepository {
	constructor({ databaseService }) {
		this.databaseService = databaseService;
	}

	async create(category) {
		throw new Error("Método create no implementado");
	}

	async findCategory(categoryParameters, trx) {
		throw new Error("Método findCategory no implementado");
	}

	async addCompetitorOnCategory({ competitor, category, trx }) {
		throw new Error("Método addCompetitorOnCategory no implementado");
	}
}
