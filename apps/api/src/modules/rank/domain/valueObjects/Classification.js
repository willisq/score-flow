export class Classification {
	constructor(value) {
		if (typeof value !== "number" || !Number.isInteger(value)) {
			throw new Error("La clasificación debe ser un número entero.");
		}
		if (value <= 0) {
			throw new Error("La clasificación debe ser un número positivo.");
		}
		this.value = value;
	}
}