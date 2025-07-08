export class findAllCategories {
	constructor({ categoryRepository }) {
		this.categoryRepository = categoryRepository;
	}

	async execute() {
		return await this.categoryRepository.findAllCategories();
	}
}
