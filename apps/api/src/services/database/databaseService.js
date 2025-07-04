import { env } from "node:process";
import knex from "knex";

const databaseConfig = {
	client: env.DB_CLIENT,
	connection: {
		host: env.DB_HOST,
		port: env.DB_PORT,
		user: env.DB_USER,
		password: env.DB_PASSWORD,
		database: env.DB_NAME,
	},
};

export const databaseService = knex(databaseConfig);
