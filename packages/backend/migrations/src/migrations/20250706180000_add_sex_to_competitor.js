/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const up = async (knex) => {
	await knex.schema.alterTable("competitor", (table) => {
		table
			.uuid("sex")
			.notNullable()
			.references("id")
			.inTable("sex")
			.onDelete("RESTRICT");
	});
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const down = async (knex) => {
	await knex.schema.alterTable("competitor", (table) => {
		table.dropColumn("sex");
	});
};