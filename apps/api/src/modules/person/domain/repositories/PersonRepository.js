export class PersonRepository {
	constructor({databaseService}) {
		this.databaseService = databaseService;
	}

	async create(person) {
		throw new Error("Método create no implementado");
	}

	async findById(id) {
		throw new Error("Método findById no implementado");
	}
}
