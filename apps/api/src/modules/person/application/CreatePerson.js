import { randomUUID } from 'crypto';

import { Person } from "#person/domain/entities/Person.js";
import { Firstname } from "#person/domain/valuesObjects/Firstname.js";
import { Lastname } from "#person/domain/valuesObjects/Lastname.js";

export class CreatePerson {
	constructor({ personRepository }) {
		this.personRepository = personRepository;
	}

	async execute({ firstname, lastname }) {
		const person = new Person({
			id: randomUUID(),
			firstname: new Firstname(firstname),
			lastname: new Lastname(lastname),
		});

		return await this.personRepository.create(person);
	}
}
