import { randomUUID } from "crypto";

import { Round } from "#round/domain/entities/Round.js";
import { Description } from "#round/domain/valueObjects/Description.js";

export class CreateRound {
	constructor({ repository }) {
		this.repository = repository;
	}

	async execute({ description }) {
		const round = new Round({
			id: randomUUID(),
			description: new Description(description),
		});

		return this.repository.create(round);
	}
}
