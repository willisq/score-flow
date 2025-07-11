import { CompetitorRepository } from "#competitor/domain/repository/CompetitorRepository.js";
import { CompetitorCategory } from "../domain/entities/CompetitorCategory.js";

export class CompetitorDatabaseRepository extends CompetitorRepository {
  tableName = "competitor";

  async create(competitor, trx = null) {
    const competitorData = competitor.toJSON();
    const db = trx || this.databaseService;

    const [createdCompetitor] = await db(this.tableName)
      .insert(competitorData)
      .returning("*");

    return createdCompetitor;
  }

  async findCompetitorCategory({ championship, category }) {
    const records = await this.databaseService("competitor_category")
      .join("competitor as com", "competitor_category.competitor", "com.id")
      .where({ championship, category })
      .select("competitor_category.id", "com.academy");

    return records;
  }

  async findCompetitorsByCategory(categoryId, championshipId) {
    const competitorsData = await this.databaseService(
      "competitor_category as cc"
    )
      .select(
        "c.id",
        "c.weight",
        "c.height",
        "c.age",
        "c.special_condition",
        "c.academy",
        this.databaseService.raw(
          "json_build_object('id', p.id, 'firstname', p.firstname, 'lastname', p.lastname) as person"
        ),
        this.databaseService.raw(
          "json_build_object('id', r.id, 'description', r.description) as rank"
        ),
        this.databaseService.raw(
          "json_build_object('id', s.id, 'description', s.description) as sex"
        )
      )
      .leftJoin("competitor as c", "c.id", "cc.competitor")
      .leftJoin("person as p", "p.id", "c.student")
      .leftJoin("rank as r", "r.id", "c.rank")
      .leftJoin("sex as s", "s.id", "c.sex")
      .where({
        "cc.category": categoryId,
        "cc.championship": championshipId,
      });

    return competitorsData;
  }

  async findAll() {
    const competitorsData = await this.databaseService("competitor as c")
      .select(
        "c.id",
        "c.weight",
        "c.height",
        "c.age",
        "c.special_condition",
        this.databaseService.raw(
          "json_build_object('id', ac.id, 'name', ac.name) as academy"
        ),
        this.databaseService.raw(
          "json_build_object('id', p.id, 'firstname', p.firstname, 'lastname', p.lastname, 'name', CONCAT(p.firstname, ' ', p.lastname)) as person"
        ),
        this.databaseService.raw(
          "json_build_object('id', r.id, 'description', r.description) as rank"
        ),
        this.databaseService.raw(
          "json_build_object('id', s.id, 'description', s.description) as sex"
        )
      )
      .join("person as p", "p.id", "c.student")
      .join("rank as r", "r.id", "c.rank")
      .join("sex as s", "s.id", "c.sex")
      .join("academy as ac", "ac.id", "c.academy");

    return competitorsData;
  }
}
