/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const up = async (knex) => {
  await knex.schema.createTable("academy", (table) => {
    table.uuid("id").primary();
    table.string("name").notNullable();
    table
      .uuid("instructor")
      .notNullable()
      .references("id")
      .inTable("person")
      .onDelete("NOTHING");
    table.timestamps(true, true);
  });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const down = async (knex) => {
  await knex.schema.dropTableIfExists("academy");
};
