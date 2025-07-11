import { PyramidRepository } from "#pyramid/domain/repositories/PyramidRepository.js";

export class PyramidDatabaseRepository extends PyramidRepository {
  tableName = "pyramid";

  async createBulk(matches) {
    if (matches.length === 0) return [];

    const roundNames = [...new Set(matches.map((match) => match.roundName))];
    const rounds = await this.databaseService("round")
      .whereIn("description", roundNames)
      .select("id", "description");

    const roundMap = rounds.reduce((acc, round) => {
      acc[round.description] = round.id;
      return acc;
    }, {});

    const dataToInsert = matches.map((match) => ({
      id: match.id,
      first_competitor: match.firstCompetitor,
      second_competitor: match.secondCompetitor,
      round: roundMap[match.roundName],
    }));

    return this.databaseService(this.tableName)
      .insert(dataToInsert)
      .returning("*");
  }

  async deleteAllPyramids() {
    return this.databaseService(this.tableName).del();
  }

  async findPyramid(pyramidFilters) {
    const { championshipId, age, sexes, ranks } = pyramidFilters;

    const query = this.databaseService(`${this.tableName} as p`);

    query
      // Joins para el primer competidor
      .join("competitor_category as cc1", "p.first_competitor", "cc1.id")
      .join("competitor as comp1", "cc1.competitor", "comp1.id")
      .join("person as per1", "comp1.student", "per1.id")
      .join("academy as ac1", "comp1.academy", "ac1.id")
      // Joins para el segundo competidor (pueden ser null)
      .leftJoin("competitor_category as cc2", "p.second_competitor", "cc2.id")
      .leftJoin("competitor as comp2", "cc2.competitor", "comp2.id")
      .leftJoin("person as per2", "comp2.student", "per2.id")
      .leftJoin("academy as ac2", "comp2.academy", "ac2.id")
      // Joins para filtros y datos adicionales
      .join("category as cat", "cc1.category", "cat.id")
      .join("category_sex as cs", "cat.id", "cs.category")
      .join("category_rank as cr", "cat.id", "cr.category")
      .join("round as r", "p.round", "r.id")
      .join("modality as mod", "cat.modality", "mod.id")
      .select(
        "p.id as pyramid_id",
        "r.description as round_name",
        "cat.id as category_id",
        "cat.initial_age",
        "cat.final_age",
        "cat.initial_weight",
        "cat.final_weight",
        "cat.special_condition",
        "mod.description as modality_description",
        this.databaseService.raw(
          `(SELECT json_agg(r.description) FROM rank r JOIN category_rank cr_sub ON r.id = cr_sub.rank WHERE cr_sub.category = cat.id) as ranks`
        ),
        // Construir objeto JSON para el primer competidor
        this.databaseService.raw(
          "json_build_object('id', comp1.id, 'academy_name', ac1.name, 'name', CONCAT(per1.firstname, ' ', per1.lastname)) as first_competitor"
        ),
        // Construir objeto JSON para el segundo competidor, manejando nulos
        this.databaseService.raw(
          `CASE
						WHEN p.second_competitor IS NOT NULL THEN
							json_build_object('id', comp2.id, 'academy_name', ac2.name, 'name', CONCAT(per2.firstname, ' ', per2.lastname))
						ELSE
							NULL
					END as second_competitor`
        )
      )
      .where("cc1.championship", championshipId)
      .groupBy(
        "p.id",
        "r.description",
        "cat.id",
        "per1.firstname",
        "per1.lastname",
        "per2.firstname",
        "per2.lastname",
        "comp1.id",
        "comp2.id",
        "ac1.name",
        "ac2.name",
        "mod.description",
        "cat.initial_age",
        "cat.final_age",
        "cat.initial_weight",
        "cat.final_weight",
        "cat.special_condition"
      );

    if (age) {
      // Asumiendo que la edad debe estar en el rango de la categoría
      query
        .andWhere("cat.initial_age", "<=", age)
        .andWhere("cat.final_age", ">=", age);
    }

    if (sexes && sexes.length > 0) {
      query.whereIn("cs.sex", sexes);
    }

    if (ranks && ranks.length > 0) {
      query.whereIn("cr.rank", ranks);
    }

    return await query;
  }

  async findAll(pyramidFilters) {
    const { championshipId } = pyramidFilters;

    const query = this.databaseService(`${this.tableName} as p`);

    query
      // Joins para el primer competidor
      .join("competitor_category as cc1", "p.first_competitor", "cc1.id")
      .join("competitor as comp1", "cc1.competitor", "comp1.id")
      .join("person as per1", "comp1.student", "per1.id")
      .join("academy as ac1", "comp1.academy", "ac1.id")
      // Joins para el segundo competidor (pueden ser null)
      .leftJoin("competitor_category as cc2", "p.second_competitor", "cc2.id")
      .leftJoin("competitor as comp2", "cc2.competitor", "comp2.id")
      .leftJoin("person as per2", "comp2.student", "per2.id")
      .leftJoin("academy as ac2", "comp2.academy", "ac2.id")
      // Joins para filtros y datos adicionales
      .join("category as cat", "cc1.category", "cat.id")
      .join("category_sex as cs", "cat.id", "cs.category")
      .join("category_rank as cr", "cat.id", "cr.category")
      .join("round as r", "p.round", "r.id")
      .join("modality as mod", "cat.modality", "mod.id")
      .select(
        "p.id as pyramid_id",
        "r.description as round_name",
        "cat.id as category_id",
        "cat.initial_age",
        "cat.final_age",
        "cat.initial_weight",
        "cat.final_weight",
        "cat.special_condition",
        "mod.description as modality_description",
        this.databaseService.raw(
          `(SELECT json_agg(r.description) FROM rank r JOIN category_rank cr_sub ON r.id = cr_sub.rank WHERE cr_sub.category = cat.id) as ranks`
        ),
        // Construir objeto JSON para el primer competidor
        this.databaseService.raw(
          "json_build_object('id', comp1.id, 'academy_name', ac1.name, 'name', CONCAT(per1.firstname, ' ', per1.lastname)) as first_competitor"
        ),
        // Construir objeto JSON para el segundo competidor, manejando nulos
        this.databaseService.raw(
          `CASE
						WHEN p.second_competitor IS NOT NULL THEN
							json_build_object('id', comp2.id, 'academy_name', ac2.name, 'name', CONCAT(per2.firstname, ' ', per2.lastname))
						ELSE
							NULL
					END as second_competitor`
        )
      )
      .where("cc1.championship", championshipId)
      .groupBy(
        "p.id",
        "r.description",
        "cat.id",
        "per1.firstname",
        "per1.lastname",
        "per2.firstname",
        "per2.lastname",
        "comp1.id",
        "comp2.id",
        "ac1.name",
        "ac2.name",
        "mod.description",
        "cat.initial_age",
        "cat.final_age",
        "cat.initial_weight",
        "cat.final_weight",
        "cat.special_condition"
      );

    return await query;
  }

  async deletePyramidByCategory(category) {
    const competitorCategoryIds = this.databaseService("competitor_category")
      .select("id")
      .where("category", category);

    return await this.databaseService(this.tableName)
      .whereIn("first_competitor", competitorCategoryIds)
      .orWhereIn("second_competitor", competitorCategoryIds)
      .del();
  }
}
