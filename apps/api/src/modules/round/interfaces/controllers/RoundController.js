import { databaseService } from "#src/services/database/databaseService.js";

import { CreateRound } from "#round/application/CreateRound.js";
import { RoundDatabaseRepository } from "#round/infraestructure/RoundDatabaseRepository.js";

export class RoundController {
	static async create(req, res) {
		const repo = new RoundDatabaseRepository(databaseService);
		const useCase = new CreateRound({ repository: repo });

		const round = await useCase.execute(req.body);

		return res.status(201).json(round);
	}
}