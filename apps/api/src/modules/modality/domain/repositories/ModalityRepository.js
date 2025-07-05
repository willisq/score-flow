export class ModalityRepository {
	constructor(databaseService) {
		this.databaseService = databaseService;
	}

	async create(modality) {
		throw new Error("Método create no implementado");
	}
}