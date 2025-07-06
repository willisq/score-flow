export class CategoryRepository {
	constructor({ databaseService }) {
		this.databaseService = databaseService;
	}

	async create(category) {
		throw new Error("Método create no implementado");
	}
}
