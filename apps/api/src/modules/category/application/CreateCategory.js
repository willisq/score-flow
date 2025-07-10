import { randomUUID } from "crypto";

import { Category } from "#category/domain/entities/Category.js";
import { CategoryRank } from "#category/domain/entities/CategoryRank.js";
import { CategorySex } from "#category/domain/entities/CategorySex.js";

import { CategoryAge } from "#category/domain/valueObjects/CategoryAge.js";
import { CategoryWeight } from "#category/domain/valueObjects/CategoryWeight.js";
import { CategoryHeight } from "#category/domain/valueObjects/CategoryHeight.js";
import { CategorySpecialCondition } from "#category/domain/valueObjects/CategorySpecialCondition.js";

export class CreateBulkCategories {
  constructor({ unitOfWork }) {
    this.unitOfWork = unitOfWork;
  }

  async execute(categoriesData) {
    if (!Array.isArray(categoriesData) || categoriesData.length === 0) {
      throw new Error("Input must be a non-empty array of categories.");
    }

    return this.unitOfWork.execute(async (repos) => {
      const createdCategories = await Promise.all(
        categoriesData.map(async (data) => {
          const { categoryData, sexes, ranks } = data;

          if (!sexes || sexes.length === 0) {
            throw new Error(
              "La categoria debe poseer al menos un sexo asociado."
            );
          }
          if (!ranks || ranks.length === 0) {
            throw new Error(
              `La categoria debe poseer al menos un rango asociado.`
            );
          }

          for (const modality of data.modalities) {
            const categoryInstance = new Category({
              id: randomUUID(),
              initialAge: new CategoryAge(categoryData.initialAge),
              finalAge: new CategoryAge(categoryData.finalAge),
              initialWeight: new CategoryWeight(categoryData.initialWeight),
              finalWeight: new CategoryWeight(categoryData.finalWeight),
              initialHeight: new CategoryHeight(categoryData.initialHeight),
              finalHeight: new CategoryHeight(categoryData.finalHeight),
              specialCondition: new CategorySpecialCondition(
                categoryData.specialCondition
              ),
              modality: modality,
            });

            const createdCategory = await repos.categoryRepository.create(
              categoryInstance
            );

            const categoryWithSexes = sexes.map(
              (sex) => new CategorySex({ sex, category: categoryInstance.id })
            );

            const createdCategoriesWithSexes =
              await repos.categorySexRepository.create(categoryWithSexes);

            const categoryWithRanks = ranks.map(
              (rank) =>
                new CategoryRank({ category: categoryInstance.id, rank })
            );

            const createdCategoriesWithRanks =
              await repos.categoryRankRepository.create(categoryWithRanks);

            return {
              ...createdCategory,
              sexes: createdCategoriesWithSexes,
              ranks: createdCategoriesWithRanks,
            };
          }
        })
      );

      return createdCategories;
    });
  }
}
