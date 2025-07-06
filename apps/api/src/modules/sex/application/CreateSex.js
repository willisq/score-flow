import { randomUUID } from "crypto";

import { Sex } from "#sex/domain/entities/Sex.js";
import { Abbreviation } from "#sex/domain/valueObjects/Abbreviation.js";
import { Description } from "#sex/domain/valueObjects/Description.js";

export class CreateSex {
	constructor({ repository }) {
		this.repository = repository;
	}

	async execute({ abbreviation, description }) {
		const sex = new Sex({
			id: randomUUID(),
			abbreviation: new Abbreviation(abbreviation),
			description: new Description(description),
		});

		return this.repository.create(sex);
	}
}