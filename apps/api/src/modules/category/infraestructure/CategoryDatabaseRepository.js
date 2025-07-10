import { Category } from "#category/domain/entities/Category.js";
import { CategoryRepository } from "#category/domain/repository/CategoryRepository.js";

import { CategoryAge } from "#category/domain/valueObjects/CategoryAge.js";
import { CategoryHeight } from "#category/domain/valueObjects/CategoryHeight.js";
import { CategorySpecialCondition } from "#category/domain/valueObjects/CategorySpecialCondition.js";
import { CategoryWeight } from "#category/domain/valueObjects/CategoryWeight.js";

export class CategoryDatabaseRepository extends CategoryRepository {
  tableName = "category";

  async create(category) {
    const categoryData = category.toJSON();

    const [createdCategory] = await this.databaseService(this.tableName)
      .insert(categoryData)
      .returning("*");

    return createdCategory;
  }

  async findCategory(categoryParameters) {
    const { rank, weight, age, height, modality, specialCondition, sex } =
      categoryParameters;

    const query = this.databaseService(this.tableName)
      .select(`${this.tableName}.*`)
      .join(
        "category_sex",
        `${this.tableName}.id`,
        "=",
        "category_sex.category"
      )
      .join(
        "category_rank",
        `${this.tableName}.id`,
        "=",
        "category_rank.category"
      )
      .where("category_sex.sex", sex)
      .where("category_rank.rank", rank)
      .where("initial_weight", "<=", weight.value)
      .andWhere("final_weight", ">=", weight.value)
      .where("initial_age", "<=", age.value)
      .andWhere("final_age", ">=", age.value)
      .where({
        modality: modality,
        special_condition: specialCondition.value,
      });

    if (height.value !== null) {
      query
        .where("initial_height", "<=", height.value)
        .andWhere("final_height", ">=", height.value);
    } else {
      query.whereNull("initial_height").whereNull("final_height");
    }

    const categoryData = await query.first();

    if (!categoryData) {
      return null;
    }

    return this._toEntity(categoryData);
  }

  _toEntity(dbData) {
    return new Category({
      id: dbData.id,
      initialRank: dbData.initial_rank,
      finalRank: dbData.final_rank,
      initialWeight: new CategoryWeight(dbData.initial_weight),
      finalWeight: new CategoryWeight(dbData.final_weight),
      initialAge: new CategoryAge(dbData.initial_age),
      finalAge: new CategoryAge(dbData.final_age),
      initialHeight: new CategoryHeight(dbData.initial_height),
      finalHeight: new CategoryHeight(dbData.final_height),
      modality: dbData.modality,
      specialCondition: new CategorySpecialCondition(dbData.special_condition),
    });
  }

  async addCompetitorOnCategory({ id, competitor, category, championship }) {
    const competitorCategoryTableName = "competitor_category";

    const linkData = {
      id,
      competitor: competitor.id,
      category: category.id,
      championship,
    };

    const [createdLink] = await this.databaseService(
      competitorCategoryTableName
    )
      .insert(linkData)
      .returning("*");

    return createdLink;
  }

  async findAllCategories() {
    const categoriesData = await this.databaseService(`${this.tableName} as c`)
      .select(
        "c.*",
        this.databaseService.raw(
          "json_agg(DISTINCT s) FILTER (WHERE s.id IS NOT NULL) as sexes"
        ),
        this.databaseService.raw(
          "json_agg(DISTINCT r) FILTER (WHERE r.id IS NOT NULL) as ranks"
        ),
        this.databaseService.raw(
          "json_build_object('id', m.id, 'name', m.description) as modality_object"
        )
      )
      .leftJoin("category_sex as cs", "c.id", "cs.category")
      .leftJoin("sex as s", "cs.sex", "s.id")
      .leftJoin("category_rank as cr", "c.id", "cr.category")
      .leftJoin("rank as r", "cr.rank", "r.id")
      .leftJoin("modality as m", "c.modality", "m.id")
      .groupBy("c.id", "m.id", "m.description");

    return categoriesData.map((data) => {
      const categoryEntity = this._toEntity(data);
      const categoryJSON = categoryEntity.toJSON();

      const modality = data.modality_object.id ? data.modality_object : null;

      return {
        ...categoryJSON,
        modality,
        sexes: data.sexes || [],
        ranks: data.ranks || [],
      };
    });
  }
}
