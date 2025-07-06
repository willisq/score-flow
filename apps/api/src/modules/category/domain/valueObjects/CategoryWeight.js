export class CategoryWeight {
	constructor(value) {
		if (value === null || value === undefined) {
			throw new Error("El peso no puede ser nulo.");
		}

		const val = Number(value);
		if (isNaN(val) || value <= 0) {
			throw new Error("El peso debe ser un número positivo.");
		}

		this.value = value;
	}
}
