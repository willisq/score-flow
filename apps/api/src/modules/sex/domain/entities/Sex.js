export class Sex {
	constructor({ id, abbreviation, description }) {
		this.id = id;
		this.abbreviation = abbreviation;
		this.description = description;
	}

	toJSON() {
		return {
			id: this.id,
			abbreviation: this.abbreviation.value,
			description: this.description.value,
		};
	}
}