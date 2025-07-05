/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const up = async (knex) => {
	await knex.schema.createTable("category", (table) => {
		table.uuid("id").primary();
		table
			.uuid("initial_rank_id")
			.notNullable()
			.references("id")
			.inTable("rank")
			.onDelete("RESTRICT");
		table
			.uuid("final_rank_id")
			.notNullable()
			.references("id")
			.inTable("rank")
			.onDelete("RESTRICT");
		table.integer("initial_age").notNullable();
		table.integer("final_age").notNullable();
		table.decimal("initial_weight", 5, 2).notNullable();
		table.decimal("final_weight", 5, 2).notNullable();
		table.decimal("initial_height", 5, 2);
		table.decimal("final_height", 5, 2);
		table.boolean("special_condition").notNullable().defaultTo(false);
		table
			.uuid("modality")
			.notNullable()
			.references("id")
			.inTable("modality")
			.onDelete("RESTRICT");
		table.timestamps(true, true);
	});
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const down = async (knex) => {
	await knex.schema.dropTableIfExists("category");
};
