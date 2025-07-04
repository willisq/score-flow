import { databaseService } from "#database/databaseService.js";
import { PersonRepository } from "#person/domain/repositories/PersonRepository.js";

export class PersonDatabaseRepository extends PersonRepository {
	tableName = "person";

	async create(person) {
		const personData = person.toJSON();

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
