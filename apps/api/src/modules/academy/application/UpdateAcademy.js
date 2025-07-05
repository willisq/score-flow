export class UpdateAcademy {
  constructor({ academyRepository, personRepository }) {
    this.academyRepository = academyRepository;
    this.personRepository = personRepository;
  }

  async execute(id, { name, instructorId }) {
    const academy = await this.academyRepository.findById(id);

    if (!academy) {
      throw new Error("Academia no encontrada");
    }

    if (instructorId) {
      const instructorExists = await this.personRepository.findById(
        instructorId
      );
      if (!instructorExists) {
        throw new Error("Instructor no encontrado");
      }
      academy.changeInstructor(instructorId);
    }

    if (name) {
      academy.changeName(name);
    }

    return await this.academyRepository.update(academy);
  }
}
