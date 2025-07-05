export class Weight {
	constructor(value) {
		if (
			value === null ||
			value === undefined ||
			typeof value !== "number" ||
			value <= 0
		) {
			throw new Error("El peso debe ser un número positivo.");
		}

		this.value = value;
	}
}
