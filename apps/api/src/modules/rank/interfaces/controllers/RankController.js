import { databaseService } from "#src/services/database/databaseService.js";

import { CreateRank } from "#rank/application/CreateRank.js";
import { RankDatabaseRepository } from "#rank/infraestructure/RankDatabaseRepository.js";

export class RankController {
	static async create(req, res) {
		const repo = new RankDatabaseRepository(databaseService);
		const useCase = new CreateRank({ repository: repo });

		const ranks = await useCase.execute(req.body);
		
		return res.status(200).json(ranks);
	}
}
