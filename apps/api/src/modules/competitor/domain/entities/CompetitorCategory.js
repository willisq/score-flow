export class CompetitorCategory {
	constructor({ id, competitor, category, championship }) {
		this.id = id;
		this.competitor = competitor;
		this.category = category;
		this.championship = championship;
	}

	toJSON() {
		return {
			id: this.id,
			competitor: this.competitor,
			category: this.category,
			championship: this.championship,
		};
	}
}
