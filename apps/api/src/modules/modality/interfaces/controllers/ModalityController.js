import { CreateModality } from "#modality/application/CreateModality.js";
import { ModalityDatabaseRepository } from "#modality/infrastructure/ModalityDatabaseRepository.js";

import { databaseService } from "#src/services/database/databaseService.js";

export class ModalityController {
	static async createModality(req, res) {
		const repo = new ModalityDatabaseRepository(databaseService);
		const useCase = new CreateModality({ repository: repo });

		await useCase.execute({
			description: req.body.description,
		});

		res.status(201).json({ message: "Modalidad creada exitosamente" });
	}
}
