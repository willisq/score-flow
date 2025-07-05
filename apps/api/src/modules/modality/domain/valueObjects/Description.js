export class Description {
	constructor(value) {
		if (!value || typeof value !== "string") {
			throw new Error("La descripción es requerida y debe ser un texto.");
		}
		if (value.trim().length === 0) {
			throw new Error("La descripción no puede estar vacía.");
		}
		if (value.length > 255) {
			throw new Error("La descripción debe ser menor a 255 caracteres.");
		}
		this.value = value.trim();
	}
}