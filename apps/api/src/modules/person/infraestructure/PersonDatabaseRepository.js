import { PersonRepository } from "#person/domain/repositories/PersonRepository.js";

export class PersonDatabaseRepository extends PersonRepository {
	tableName = "person";

	async create(person, trx = null) {
		const personData = person.toJSON();
		const db = trx || this.databaseService;
		
		const [createdPerson] = await db(this.tableName)
			.insert(personData)
			.returning("*");

		return createdPerson;
	}

	async findById(id) {
		const person = await this.databaseService(this.tableName)
			.where({ id })
			.first();

		return person;
	}
}
