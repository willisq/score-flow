import { databaseService } from "#src/services/database/databaseService.js";

import { CreateSex } from "#sex/application/CreateSex.js";
import { SexDatabaseRepository } from "#sex/infraestructure/SexDatabaseRepository.js";

export class SexController {
	static async create(req, res) {
		const repo = new SexDatabaseRepository(databaseService);
		const useCase = new CreateSex({ repository: repo });

		const sex = await useCase.execute(req.body);

		return res.status(201).json(sex);
	}
}