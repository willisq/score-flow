import { randomUUID } from "crypto";

import { Person } from "#person/domain/entities/Person.js";
import { Firstname } from "#person/domain/valuesObjects/Firstname.js";
import { Lastname } from "#person/domain/valuesObjects/Lastname.js";
import { Competitor } from "#competitor/domain/entities/Competitor.js";
import { SpecialCondition } from "#competitor/domain/valueObjects/SpecialCondition.js";

export class CreateCompetitorWithPerson {
	constructor({
		competitorRepository,
		personRepository,
		databaseService,
	}) {
		this.competitorRepository = competitorRepository;
		this.personRepository = personRepository;
		this.databaseService = databaseService;
	}

	async execute({ personData, rank, academy, specialCondition = false }) {
		return this.databaseService.transaction(async (trx) => {
			const person = new Person({
				id: randomUUID(),
				firstname: new Firstname(personData.firstname),
				lastname: new Lastname(personData.lastname),
			});
			const createdPerson = await this.personRepository.create(person, trx);

			const competitor = new Competitor({
				id: randomUUID(),
				student: createdPerson.id,
				rank: rank,
				academy: academy,
				specialCondition: new SpecialCondition(specialCondition),
			});
			const createdCompetitor = await this.competitorRepository.create(
				competitor,
				trx,
			);

			return { ...createdCompetitor, person: createdPerson };
		});
	}
}
