export class Category {
	constructor(categoryData) {
		Object.assign(this, categoryData);
	}

	toJSON() {
		return {
			id: this.id,
			initial_rank: this.initialRank,
			final_rank: this.finalRank,
			initial_weight: this.initialWeight.value,
			final_weight: this.finalWeight.value,
			initial_age: this.initialAge.value,
			final_age: this.finalAge.value,
			initial_height: this.initialHeight.value,
			final_height: this.finalHeight.value,
			modality: this.modality,
			special_condition: this.specialCondition.value,
		};
	}
}
