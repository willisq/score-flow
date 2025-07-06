export class CategoryRank {
	constructor({category, rank}) {
		
		this.category = category;
		this.rank = rank;
	}

	toJSON() {
		return {
			category: this.category,
			rank: this.rank,
		};
	}
}
