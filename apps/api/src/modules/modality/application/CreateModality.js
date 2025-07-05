import { randomUUID } from "crypto";

import { Modality } from "#modality/domain/entities/Modality.js";
import { Description } from "#modality/domain/valueObjects/Description.js";

export class CreateModality {
	constructor({ repository }) {
		this.repository = repository;
	}

	async execute({ description }) {
		const modality = new Modality({
			id: randomUUID(),
			description: new Description(description),
		});

		return await this.repository.create(modality);
	}
}