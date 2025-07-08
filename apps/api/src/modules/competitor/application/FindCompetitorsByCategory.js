export class FindCompetitorsByCategory {
	constructor({ competitorRepository }) {
		this.competitorRepository = competitorRepository;
	}

	async execute({ category, championship }) {
		console.log(category, championship);

		if (!category || !championship) {
			throw new Error(
				"El ID de la categoría y el ID del campeonato son requeridos.",
			);
		}

		const competitors = await this.competitorRepository.findCompetitorsByCategory(
			category,
			championship,
		);

		return competitors;
	}
}
