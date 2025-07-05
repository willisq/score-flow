export class Age {
	constructor(value) {
		if (value === null || value === undefined) {
			this.value = null;
			return;
		}

		if (value === null || value === undefined || !Number.isInteger(value)) {
			throw new Error("La edad debe ser un número entero.");
		}

		this.value = value;
	}
}
