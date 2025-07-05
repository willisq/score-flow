export class FindAcademy {
	constructor({ academyRepository }) {
		this.academyRepository = academyRepository;
	}

	async execute(params) {
		const { id, name, instructorId, instructorName } = params;
		if (id) {
			return await this.academyRepository.findById(id);
		}

		if (name) {
			return await this.academyRepository.findByName(name);
		}

		if (instructorId) {
			return await this.academyRepository.findByInstructorId(instructorId);
		}

		if (instructorName) {
			return await this.academyRepository.findByInstructorName(instructorName);
		}

		return await this.academyRepository.findAll();
	}
}
