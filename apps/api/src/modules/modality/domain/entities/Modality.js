export class Modality {
	constructor({ id, description }) {
		this.id = id;
		this.description = description;
	}

	toJSON() {
		return {
			id: this.id,
			description: this.description.value,
		};
	}
}