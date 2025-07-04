export class Academy {
	constructor({ name, person }) {
		this.name = name;
		this.person = person;
	}

	toJSON() {
		return {
			name: this.name.value,
			person: this.person.toJSON(),
		};
	}
}
