/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export const up = async (knex) => {
	await knex.schema.createTable("category_sex", (table) => {
		table
			.uuid("sex")
			.notNullable()
			.references("id")
			.inTable("sex")
			.onDelete("RESTRICT");
		table
			.uuid("category")
			.notNullable()
			.references("id")
			.inTable("category")
			.onDelete("RESTRICT");
		table.primary(["sex", "category"]);
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
