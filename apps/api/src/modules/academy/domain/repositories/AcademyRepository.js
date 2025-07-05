export class AcademyRepository {
	constructor(databaseService) {
		this.databaseService = databaseService;
	}

	async create(academy) {
		throw new Error("Método create no implementado");
	}

	async findById(id) {
		throw new Error("Método findById no implementado");
	}

	async findByName(name) {
		throw new Error("Método findByName no implementado");
	}

	async update(academy) {
		throw new Error("Método update no implementado");
	}

	async delete(id) {
		throw new Error("Método delete no implementado");
	}

	async findAll() {
		throw new Error("Método findAll no implementado");
	}

	async findByInstructorId(instructorId) {
		throw new Error("Método findByInstructorId no implementado");
	}

	async findByInstructorName(instructorName) {
		throw new Error("Método findByInstructorName no implementado");
	}
}
