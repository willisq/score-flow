export class Height {
	constructor(value) {
        if (value === null || value === undefined) {
            this.value = null;
            return;
        }

		if (!Number.isInteger(value) || value < 0) {
			throw new Error("La altura debe ser un número valido.");
		}

		this.value = value;
	}
}
