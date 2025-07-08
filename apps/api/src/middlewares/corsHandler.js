import { env } from "node:process";

import cors from "cors";

const whitelist = [env.FRONTEND_URL];

const corsOptions = {
	origin: (origin, callback) => {
		if (!origin || whitelist.includes(origin)) {
			callback(null, true);
		} else {
			callback(new Error("No permitido por CORS"));
		}
	},
};

export const corsMiddleware = cors(corsOptions);
