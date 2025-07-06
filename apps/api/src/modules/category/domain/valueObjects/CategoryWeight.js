export class CategoryWeight {
	constructor(value) {
		if (value === null || value === undefined) {
			throw new Error("El peso no puede ser nulo.");
		}
		if (typeof value !== "number" || value <= 0) {
			throw new Error("El peso debe ser un número positivo.");
		}

		this.value = value;
	}
}