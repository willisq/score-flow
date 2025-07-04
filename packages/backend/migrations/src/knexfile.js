import "dotenv/config";

import path from "node:path";

import { env } from "node:process";

export default {
	client: env.DB_CLIENT,
	connection: {
		host: env.DB_HOST,
		port: env.DB_PORT,
		user: env.DB_USER,
		password: env.DB_PASSWORD,
		database: env.DB_NAME,
	},
	migrations: {
		directory: path.join(import.meta.dirname, "migrations"),
	},
};
