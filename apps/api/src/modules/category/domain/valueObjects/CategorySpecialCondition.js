export class CategorySpecialCondition {
	constructor(value) {
		if (value === null || value === undefined) {
			this.value = false;
			return;
		}

		if (typeof value !== "boolean") {
			throw new Error("La condición especial debe ser un valor booleano (true o false).");
		}

		this.value = value;
	}
}