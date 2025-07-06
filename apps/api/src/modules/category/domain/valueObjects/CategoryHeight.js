export class CategoryHeight {
	constructor(value) {
		if (value === null || value === undefined) {
			this.value = null;
			return;
		}

		if (typeof value !== "number" || value < 0) {
			throw new Error("La altura debe ser un número válido.");
		}

		this.value = value;
	}
}