export class Abbreviation {
	constructor(value) {
        console.log(value);
        
		if (!value || typeof value !== "string" || value.trim().length === 0) {
			throw new Error("La abreviatura es obligatoria.");
		}
		if (value.length > 10) {
			throw new Error("La abreviatura no puede exceder los 10 caracteres.");
		}

		this.value = value.trim();
	}
}