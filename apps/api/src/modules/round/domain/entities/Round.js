export class Round {
	constructor({ id, description }) {
		this.id = id;
		this.description = description;
	}

	static create({ id, description }) {
		return new Round({ id, description });
	}

	toJSON() {
		return {
			id: this.id,
			description: this.description.value,
		};
	}
}