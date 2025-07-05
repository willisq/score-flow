import { databaseService } from "#src/services/database/databaseService.js";

import { FindAcademy } from "#academy/application/FindAcademy.js";

import { AcademyDatabaseRepository } from "#academy/infraestructure/AcademyDatabaseRepository.js";
import { PersonDatabaseRepository } from "#person/infraestructure/PersonDatabaseRepository.js";
import { CreateAcademyWithInstructor } from "#academy/application/CreateAcademyWithInstructor.js";
export class AcademyController {
	static async createAcademy(req, res) {
		const academyRepo = new AcademyDatabaseRepository(databaseService);
		const personRepo = new PersonDatabaseRepository(databaseService);

		const useCase = new CreateAcademyWithInstructor({
			academyRepository: academyRepo,
			personRepository: personRepo,
			databaseService: databaseService,
		});

		const createdAcademy = await useCase.execute({
			name: req.body.name,
			instructorData: req.body.instructor,
		});

		return res.status(201).json(createdAcademy);
	}

	static async delete(req, res) {}

	static async update(req, res) {}

	static async getById(req, res) {}

	static async getAll(req, res) {
		const academyRepo = new AcademyDatabaseRepository(databaseService);

		const findAcademy = new FindAcademy({ academyRepository: academyRepo });

		const { id, name, instructorId, instructorName } = req.query;

		const academies = await findAcademy.execute({
			id,
			name,
			instructorId,
			instructorName,
		});

		return res.status(200).json(academies);
	}
}
