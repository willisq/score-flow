/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export function up(knex) {
	return knex.schema.createTable("category_rank", (table) => {
		table
			.uuid("category")
			.notNullable()
			.references("id")
			.inTable("category")
			.onDelete("RESTRICT");
		table
			.uuid("rank")
			.notNullable()
			.references("id")
			.inTable("rank")
			.onDelete("RESTRICT");

		table.primary(["category", "rank"]);

		table.timestamps(true, true);
	});
}

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export function down(knex) {
	return knex.schema.dropTable("category_rank");
}
