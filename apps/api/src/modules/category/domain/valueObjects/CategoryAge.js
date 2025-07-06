export class CategoryAge {
	constructor(value) {
		if (value === null || value === undefined) {
			throw new Error("La edad no puede ser nula.");
		}

		if (!Number.isInteger(value) || value < 0) {
			throw new Error("La edad debe ser un número entero positivo.");
		}

		this.value = value;
	}
}