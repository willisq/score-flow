export class FindAllModalities {
  constructor({ modalityRepository }) {
    this.modalityRepository = modalityRepository;
  }

  async execute() {
    return this.modalityRepository.findAll();
  }
}
