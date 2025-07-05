export class SpecialCondition {
	constructor(value) {
		// Si el valor no se proporciona (es nulo o indefinido),
		// se establece el valor por defecto `false`, como en la base de datos.
		if (value === null || value === undefined) {
			this.value = false;
			return;
		}

		// Si se proporciona un valor, debe ser un booleano.
		if (typeof value !== "boolean") {
			throw new Error("La condición especial debe ser un valor booleano (true o false).");
		}

		this.value = value;
	}
}