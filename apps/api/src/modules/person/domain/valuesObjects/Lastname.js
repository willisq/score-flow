export class Lastname {
	constructor(value) {
		if (value.length > 250) {
			throw new Error("El apellido debe ser menor a 250 caracteres");
		}

		this.value = value.trim();
	}
}
