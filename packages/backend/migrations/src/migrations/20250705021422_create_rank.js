/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const up = async (knex) => {
	await knex.schema.createTable("rank", (table) => {
		table.uuid("id").primary();
		table.string("description").notNullable();
		table.integer("classification").notNullable();
		table.boolean("is_back_belt").notNullable().defaultTo(false);
		table.timestamps(true, true);
	});
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const down = async (knex) => {
	await knex.schema.dropTableIfExists("rank");
};
