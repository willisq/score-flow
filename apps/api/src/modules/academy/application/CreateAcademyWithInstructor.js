import { randomUUID } from "crypto";

import { Academy } from "#academy/domain/entities/Academy.js";
import { Name } from "#academy/domain/valueObjects/Name.js";
import { Person } from "#person/domain/entities/Person.js";
import { Firstname } from "#person/domain/valuesObjects/Firstname.js";
import { Lastname } from "#person/domain/valuesObjects/Lastname.js";

export class CreateAcademyWithInstructor {
	constructor({ academyRepository, personRepository, databaseService }) {
		this.academyRepository = academyRepository;
		this.personRepository = personRepository;
		this.databaseService = databaseService;
	}

	async execute({ name, instructorData }) {
		return this.databaseService.transaction(async (trx) => {
			const person = new Person({
				id: randomUUID(),
				firstname: new Firstname(instructorData.firstname),
				lastname: new Lastname(instructorData.lastname),
			});

			const createdPerson = await this.personRepository.create(person, trx);

			const academy = new Academy({
				id: randomUUID(),
				name: new Name(name),
				instructor: createdPerson.id,
			});

			const createdAcademy = await this.academyRepository.create(academy, trx);
			return createdAcademy;
		});
	}
}
