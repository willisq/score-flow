export class FindAllCompetitors {
  constructor({ competitorRepository }) {
    this.competitorRepository = competitorRepository;
  }

  async execute() {
    const competitors = await this.competitorRepository.findAll();

    return competitors;
  }
}
