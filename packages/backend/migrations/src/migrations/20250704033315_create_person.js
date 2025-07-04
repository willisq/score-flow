/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const up = async (knex) =>{
  await knex.schema.createTable("person", (table) => {
		table.uuid("id").primary();
		table.string("firstname").notNullable();
		table.string("lastname").notNullable();
		table.timestamps(true, true);
	});
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const down = async (knex)=> {
  await knex.schema.dropTableIfExists("person");
};
