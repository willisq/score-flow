export class FindAllSexes {
  constructor({ sexRepository }) {
    this.sexRepository = sexRepository;
  }

  async execute() {
    return this.sexRepository.findAll();
  }
}
