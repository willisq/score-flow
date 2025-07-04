export class Person {
	constructor({ id, firstname, lastname }) {
		this.id = id;
		this.firstname = firstname;
		this.lastname = lastname;
	}

	toJSON() {
		return {
			id: this.id,
			firstname: this.firstname.value,
			lastname: this.lastname.value,
		};
	}
}
