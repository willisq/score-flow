import { databaseService } from "#src/services/database/databaseService.js";

import { CreateCompetitorWithPerson } from "#competitor/application/CreateCompetitorWithPerson.js";
import { CreateBulkCompetitorsWithPersons } from "#competitor/application/CreateBulkCompetitorsWithPersons.js";

import { CompetitorDatabaseRepository } from "#competitor/infraestructure/CompetitorDatabaseRepository.js";
import { PersonDatabaseRepository } from "#person/infraestructure/PersonDatabaseRepository.js";

export class CompetitorController {
	static async create(req, res) {
		const useCase = new CreateCompetitorWithPerson({
			competitorRepository: new CompetitorDatabaseRepository(databaseService),
			personRepository: new PersonDatabaseRepository(databaseService),
			databaseService: databaseService,
		});

		const createdCompetitor = await useCase.execute(req.body);

		return res.status(201).json(createdCompetitor);
	}

	static async createBulk(req, res) {
		const useCase = new CreateBulkCompetitorsWithPersons({
			competitorRepository: new CompetitorDatabaseRepository(databaseService),
			personRepository: new PersonDatabaseRepository(databaseService),
			databaseService: databaseService,
		});

		const createdCompetitors = await useCase.execute(req.body);

		return res.status(201).json(createdCompetitors);
	}
}
