export class Category {
	constructor(categoryData) {
		const {
			id,
			initialWeight,
			finalWeight,
			initialAge,
			finalAge,
			initialHeight,
			finalHeight,
			modality,
			specialCondition,
		} = categoryData;

		this.id = id;
		this.initialWeight = initialWeight;
		this.finalWeight = finalWeight;
		this.initialAge = initialAge;
		this.finalAge = finalAge;
		this.initialHeight = initialHeight;
		this.finalHeight = finalHeight;
		this.modality = modality;
		this.specialCondition = specialCondition;
	}

	toJSON() {
		return {
			id: this.id,
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
