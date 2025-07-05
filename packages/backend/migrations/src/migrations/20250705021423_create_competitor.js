/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const up = async (knex) => {
	await knex.schema.createTable("competitor", (table) => {
		table.uuid("id").primary();
		table
			.uuid("rank")
			.notNullable()
			.references("id")
			.inTable("rank")
			.onDelete("RESTRICT");
		table
			.uuid("academy")
			.notNullable()
			.references("id")
			.inTable("academy")
			.onDelete("RESTRICT");
		table.boolean("special_condition").notNullable().defaultTo(false);
		table.timestamps(true, true);
	});
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const down = async (knex) => {
	await knex.schema.dropTableIfExists("competitor");
};
