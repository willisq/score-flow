/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const up = async (knex) => {
	await knex.schema.createTable("category", (table) => {
		table.uuid("id").primary();
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

	await knex.raw(
		`ALTER TABLE category ADD CONSTRAINT uq_category UNIQUE NULLS NOT DISTINCT (initial_age, final_age, initial_weight, final_weight, initial_height, final_height, special_condition, modality)`,
	);
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const down = async (knex) => {
	await knex.schema.dropTableIfExists("category");
};
