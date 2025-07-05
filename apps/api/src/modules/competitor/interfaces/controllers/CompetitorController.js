import { databaseService } from "#src/services/database/databaseService.js";

import { CreateCompetitorWithPerson } from "#competitor/application/CreateCompetitorWithPerson.js";

import { CompetitorDatabaseRepository } from "#competitor/infraestructure/CompetitorDatabaseRepository.js";
import { PersonDatabaseRepository } from "#person/infraestructure/PersonDatabaseRepository.js";

export class CompetitorController {
	static async create(req, res, next) {
		const useCase = new CreateCompetitorWithPerson({
			competitorRepository: new CompetitorDatabaseRepository(databaseService),
			personRepository: new PersonDatabaseRepository(databaseService),
			databaseService: databaseService,
		});

		const createdCompetitor = await useCase.execute(req.body);

		return res.status(201).json(createdCompetitor);
	}
}
