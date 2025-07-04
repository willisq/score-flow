import { databaseService } from "#database/databaseService.js";
import { PersonRepository } from "#person/domain/repositories/PersonRepository.js";

export class PersonDatabaseRepository extends PersonRepository {
	tableName = "person";

	async create(person) {
		const personAsJSON = person.toJSON();
		const personData = {
			person_firstname_de: personAsJSON.firstname,
			person_lastname_de: personAsJSON.lastname,
		};

		const [createdPerson] = await databaseService(this.tableName)
			.insert(personData)
			.returning("*");

		return createdPerson;
	}

	async findById(id) {
		const person = await databaseService(this.personModel.tableName)
			.where({ id })
			.first();

		return person;
	}
}
