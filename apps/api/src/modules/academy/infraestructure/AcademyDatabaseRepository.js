import { AcademyRepository } from "#academy/domain/repositories/AcademyRepository.js";

export class AcademyDatabaseRepository extends AcademyRepository {
    tableName = "academy";

    constructor(databaseService) {
        this.databaseService = databaseService;
    }

    async create(academy) {
        const academyAsJSON = academy.toJSON();
        const academyData = {
            academy_name_de: academyAsJSON.name,
            person_id: academyAsJSON.person.id,
        };

        const [createdAcademy] = await this.databaseService(this.tableName)
            .insert(academyData)
            .returning("*");

        return createdAcademy;
    }

    async findById(id) {
    }

    async findByName(name) {
    }

    async update(academy) {
    }

    async delete(id) {
    }
}