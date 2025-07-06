import { randomUUID } from "crypto";

import { CategorySex } from "#category/domain/entities/CategorySex.js";
import { CategoryAge } from "#category/domain/valueObjects/CategoryAge.js";
import { CategoryWeight } from "#category/domain/valueObjects/CategoryWeight.js";
import { CategoryHeight } from "#category/domain/valueObjects/CategoryHeight.js";
import { CategorySpecialCondition } from "#category/domain/valueObjects/CategorySpecialCondition.js";
import { Category } from "#category/domain/entities/Category.js";

export class CreateCategoryWithSexes {
	constructor({ categoryRepository, categorySexRepository }) {
		this.categoryRepository = categoryRepository;
		this.categorySexRepository = categorySexRepository;
	}

	async execute({ category, sexes }) {
		if (!Array.isArray(sexes)) {
			throw new Error("Debe indicar los sexos permitidos para la categoría");
		}

		const categoryInstance = new Category({
			id: randomUUID(),
			initialRank: category.initialRank,
			finalRank: category.finalRank,
			initialAge: new CategoryAge(category.initialAge),
			finalAge: new CategoryAge(category.finalAge),
			initialWeight: new CategoryWeight(category.initialWeight),
			finalWeight: new CategoryWeight(category.finalWeight),
			initialHeight: new CategoryHeight(category.initialHeight),
			finalHeight: new CategoryHeight(category.finalHeight),
			specialCondition: new CategorySpecialCondition(category.specialCondition),
			modality: category.modality,
		});

		const createdCategory =
			await this.categoryRepository.create(categoryInstance);

		const categorySexes = sexes.map(
			(sex) => new CategorySex({ category: categoryInstance.id, sex: sex }),
		);

		const createdCategorySex =
			await this.categorySexRepository.createCategoryWithSexes(categorySexes);

		return { ...createdCategory, category_sex: createdCategorySex };
	}
}
