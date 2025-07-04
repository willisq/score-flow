export class Firstname {
	constructor(value) {
		if (value.length > 250) {
			throw new Error("El nombre debe ser menor a 250 caracteres");
		}

		this.value = value.trim();
	}
}
