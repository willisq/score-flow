import { randomUUID } from "crypto";

import { Person } from "#person/domain/entities/Person.js";
import { Firstname } from "#person/domain/valuesObjects/Firstname.js";
import { Lastname } from "#person/domain/valuesObjects/Lastname.js";
import { Competitor } from "#competitor/domain/entities/Competitor.js";

import { Weight } from "#competitor/domain/valueObjects/Weight.js";
import { Age } from "#competitor/domain/valueObjects/Age.js";
import { Height } from "#competitor/domain/valueObjects/Height.js";
import { SpecialCondition } from "#competitor/domain/valueObjects/SpecialCondition.js";

export class CreateBulkCompetitorsWithPersons {
	constructor({ competitorRepository, personRepository, databaseService }) {
		this.competitorRepository = competitorRepository;
		this.personRepository = personRepository;
		this.databaseService = databaseService;
	}

	async execute(competitorsData) {
		if (!Array.isArray(competitorsData) || competitorsData.length === 0) {
			throw new Error("Input must be a non-empty array of competitors.");
		}

		return this.databaseService.transaction(async (trx) => {
			const createdRecords = await Promise.all(
				competitorsData.map(async (data) => {
					const {
						personData,
						rank,
						academy,
						weight,
						height = null,
						age,
						specialCondition = false,
					} = data;

					const person = new Person({
						id: randomUUID(),
						firstname: new Firstname(personData.firstname),
						lastname: new Lastname(personData.lastname),
					});
					const createdPerson = await this.personRepository.create(person, trx);

					const competitor = new Competitor({
						id: randomUUID(),
						student: createdPerson.id,
						rank,
						academy,
						specialCondition: new SpecialCondition(specialCondition),
						height: new Height(height),
						weight: new Weight(weight),
						age: new Age(age),
					});
					const createdCompetitor =
						await this.competitorRepository.create(competitor, trx);

					return { ...createdCompetitor, person: createdPerson };
				}),
			);

			return createdRecords;
		});
	}
}