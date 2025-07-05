export class Rank {
	constructor({ id, description, classification, is_back_belt }) {
		this.id = id;
		this.description = description;
		this.classification = classification;
		this.is_back_belt = is_back_belt;
	}

	static create({ id, description, classification, is_back_belt }) {
		return new Rank({ id, description, classification, is_back_belt });
	}

	toJSON() {
		return {
			id: this.id,
			description: this.description.value,
			classification: this.classification.value,
			is_back_belt: this.is_back_belt,
		};
	}
}