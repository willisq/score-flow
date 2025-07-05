import { CreatePerson } from "#person/application/CreatePerson.js";
import { PersonDatabaseRepository } from "#person/infraestructure/PersonDatabaseRepository.js";

import { databaseService } from "#src/services/database/databaseService.js";

export class PersonController {
	static async createPerson(req, res) {
		const repo = new PersonDatabaseRepository(databaseService);
		const useCase = new CreatePerson({ personRepository: repo });

		await useCase.execute({
			firstname: req.body.firstname,
			lastname: req.body.lastname,
		});

		res.status(201).json({ message: "Persona creada exitosamente" });
	}
}
