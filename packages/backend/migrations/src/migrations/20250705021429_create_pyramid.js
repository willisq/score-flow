/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const up = async (knex) => {
	await knex.schema.createTable("pyramid", (table) => {
		table.uuid("id").primary();
		table
			.uuid("round_id")
			.notNullable()
			.references("id")
			.inTable("round")
			.onDelete("RESTRICT");
		table
			.uuid("first_competitor_id")
			.notNullable()
			.references("id")
			.inTable("competitor_category")
			.onDelete("RESTRICT");
		table
			.uuid("second_competitor_id")
			.nullable()
			.references("id")
			.inTable("competitor_category")
			.onDelete("RESTRICT");
		table
			.uuid("winner_competitor_id")
			.nullable()
			.references("id")
			.inTable("competitor_category")
			.onDelete("RESTRICT");
		table.timestamps(true, true);
		table.unique(["first_competitor_id", "round_id"]);
		table.unique(["second_competitor_id", "round_id"]);
	});
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const down = async (knex) => {
	await knex.schema.dropTableIfExists("pyramid");
};