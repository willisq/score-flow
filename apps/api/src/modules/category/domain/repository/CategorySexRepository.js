export class CategorySexRepository {
	constructor({databaseService} ) {
		this.databaseService = databaseService;
	}

	async createCategoryWithSexes(categorySexes, trx) {
		throw new Error("Método createCategoryWithSexes no implementado");
	}
}
