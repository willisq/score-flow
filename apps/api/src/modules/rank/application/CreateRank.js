import { randomUUID } from "crypto";

import { Rank } from "#rank/domain/entities/Rank.js";

import { Description } from "#rank/domain/valueObjects/Description.js";
import { Classification } from "#rank/domain/valueObjects/Classification.js";

export class CreateRank {
	constructor({ repository }) {
		this.repository = repository;
	}

	async execute({ description, classification, is_back_belt = false }) {
		const rankDescription = new Description(description);
		const rankClassification = new Classification(classification);

		const rank = new Rank({
			id: randomUUID(),
			description: rankDescription,
			classification: rankClassification,
			is_back_belt: is_back_belt,
		});
		
		return this.repository.create(rank);
	}
}