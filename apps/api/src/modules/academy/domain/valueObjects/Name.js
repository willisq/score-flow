export class Name {
	constructor(name) {
		if (!name || typeof name !== "string" || name.trim() === "") {
			throw new Error("Name must be a non-empty string");
		}

		this.name = name;
	}

	get value() {
		return this.name;
	}
}
