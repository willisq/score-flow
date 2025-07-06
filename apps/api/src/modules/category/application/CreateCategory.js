import { randomUUID } from "crypto";
import { Category } from "#category/domain/entities/Category.js";
import { CategoryAge } from "#category/domain/valueObjects/CategoryAge.js";
import { CategoryWeight } from "#category/domain/valueObjects/CategoryWeight.js";
import { CategoryHeight } from "#category/domain/valueObjects/CategoryHeight.js";
import { CategorySpecialCondition } from "#category/domain/valueObjects/CategorySpecialCondition.js";

export class CreateCategory {
	constructor({ categoryRepository, databaseService }) {
		this.categoryRepository = categoryRepository;
	}

	async execute({
		initialRank,
		finalRank,
		initialAge,
		finalAge,
		initialWeight,
		finalWeight,
		initialHeight = null,
		finalHeight = null,
		specialCondition = false,
		modality,
	}) {
		const category = new Category({
			id: randomUUID(),
			initialRank,
			finalRank,
			initialAge: new CategoryAge(initialAge),
			finalAge: new CategoryAge(finalAge),
			initialWeight: new CategoryWeight(initialWeight),
			finalWeight: new CategoryWeight(finalWeight),
			initialHeight: new CategoryHeight(initialHeight),
			finalHeight: new CategoryHeight(finalHeight),
			specialCondition: new CategorySpecialCondition(specialCondition),
			modality,
		});

		const createdCategory = await this.categoryRepository.create(category);

		return createdCategory;
	}
}
