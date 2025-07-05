import { ModalityRepository } from "#modality/domain/repositories/ModalityRepository.js";

export class ModalityDatabaseRepository extends ModalityRepository {
	tableName = "modality";

	async create(modality, trx = null) {
		const modalityData = modality.toJSON();
		const db = trx || this.databaseService;

		const [createdModality] = await db(this.tableName)
			.insert(modalityData)
			.returning("*");

		return createdModality;
	}
}