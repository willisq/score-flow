export class DeleteAcdemy {
  constructor({ academyRepository }) {
    this.academyRepository = academyRepository;
  }

  async execute(id) {
    return await this.academyRepository.delete(id);
  }
}
