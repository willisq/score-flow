/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const up = async (knex) => {
	await knex.schema.createTable("competitor", (table) => {
		table.uuid("id").primary();
		table
			.uuid("student")
			.notNullable()
			.unique()
			.references("id")
			.inTable("person")
			.onDelete("RESTRICT");
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
		table
			.uuid("sex")
			.notNullable()
			.references("id")
			.inTable("sex")
			.onDelete("RESTRICT");
		table.integer("age").notNullable();
		table.decimal("weight", 5, 2).notNullable();
		table.decimal("height", 5, 2);
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
