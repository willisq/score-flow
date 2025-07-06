/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const up = async (knex) => {
	await knex.schema.createTable("category_sex", (table) => {
		table
			.uuid("sex_id")
			.notNullable()
			.references("id")
			.inTable("sex")
			.onDelete("RESTRICT");
		table
			.uuid("category_id")
			.notNullable()
			.references("id")
			.inTable("category")
			.onDelete("RESTRICT");
		table.primary(["sex_id", "category_id"]);
		table.timestamps(true, true);
	});
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const down = async (knex) => {
	await knex.schema.dropTableIfExists("category_sex");
};
