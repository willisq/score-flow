/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const up = async (knex) => {
	await knex.schema.createTable("pyramid", (table) => {
		table.uuid("id").primary();
		table
			.uuid("round")
			.notNullable()
			.references("id")
			.inTable("round")
			.onDelete("RESTRICT");
		table
			.uuid("first_competitor")
			.notNullable()
			.references("id")
			.inTable("competitor_category")
			.onDelete("RESTRICT");
		table
			.uuid("second_competitor")
			.nullable()
			.references("id")
			.inTable("competitor_category")
			.onDelete("RESTRICT");
		table
			.uuid("winner")
			.nullable()
			.references("id")
			.inTable("competitor_category")
			.onDelete("RESTRICT");
		table.timestamps(true, true);
		table.unique(["first_competitor", "round"]);
		table.unique(["second_competitor", "round"]);
	});
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const down = async (knex) => {
	await knex.schema.dropTableIfExists("pyramid");
};
