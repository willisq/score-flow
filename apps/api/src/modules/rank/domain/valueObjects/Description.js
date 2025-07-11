export class Description {
	constructor(value) {
		if (!value || typeof value !== "string" || value.trim().length === 0) {
			throw new Error("La descripción es obligatoria.");
		}
		if (value.length > 255) {
			throw new Error("La descripción no puede exceder los 255 caracteres.");
		}

		this.value = value.trim();
	}
}