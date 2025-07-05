import { AcademyRepository } from "#academy/domain/repositories/AcademyRepository.js";

export class AcademyDatabaseRepository extends AcademyRepository {
	tableName = "academy";

	async create(academy, trx = null) {
		const academyData = academy.toJSON();
		const db = trx || this.databaseService;

		const [createdAcademy] = await db(this.tableName)
			.insert(academyData)
			.returning("*");

		return createdAcademy;
	}

	async findAll(trx = null) {
		const db = trx || this.databaseService;
		const academies = await db(this.tableName).select("*");

		return academies;
	}

	async findById(id, trx = null) {
		const db = trx || this.databaseService;
		const academy = await db(this.tableName).where({ id }).first();

		return academy;
	}

	async findByName(name, trx = null) {
		const db = trx || this.databaseService;
		
		const academy = await db(this.tableName).where(
			"name",
			"ilike",
			`%${name}%`,
		);

		return academy;
	}

	async findByInstructorId(instructorId, trx = null) {
		const db = trx || this.databaseService;
		const academy = await db(this.tableName)
			.where({ instructor: instructorId })
			.first();

		return academy;
	}

	async findByInstructorName(instructorName, trx = null) {
		const db = trx || this.databaseService;
		const academy = await db(this.tableName)
			.join("person", "academy.instructor", "=", "person.id")
			.select("academy.*")
			.where("person.firstname", "like", `%${instructorName}%`)
			.first();

		return academy;
	}

	async update(id, { name, instructorId }, trx = null) {
		const academyData = {};
		const db = trx || this.databaseService;

		if (name) {
			academyData.name = name.value;
		}
		if (instructorId) {
			academyData.instructor = instructorId;
		}

		const [updatedAcademy] = await db(this.tableName)
			.where({ id })
			.update(academyData)
			.returning("*");

		return updatedAcademy;
	}

	async delete(id, trx = null) {
		const db = trx || this.databaseService;
		const deletedCount = await db(this.tableName).where({ id }).del();

		return deletedCount > 0;
	}
}
