/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const up = async (knex) => {
	await knex.schema.createTable("competitor_category", (table) => {
		table.uuid("id").primary();
		table
			.uuid("competitor")
			.notNullable()
			.references("id")
			.inTable("competitor")
			.onDelete("RESTRICT");
		table
			.uuid("category")
			.notNullable()
			.references("id")
			.inTable("category")
			.onDelete("RESTRICT");
		table
			.uuid("championship")
			.nullable()
			.references("id")
			.inTable("championship")
			.onDelete("RESTRICT");
		table.timestamps(true, true);
		table.unique(["competitor", "category", "championship"]);
	});
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const down = async (knex) => {
	await knex.schema.dropTableIfExists("competitor_category");
};