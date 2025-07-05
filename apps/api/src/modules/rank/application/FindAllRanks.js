export class FindAllRanks {
	constructor({ rankRepository }) {
		this.rankRepository = rankRepository;
	}

	async execute() {
		return this.rankRepository.findAll();
	}
}