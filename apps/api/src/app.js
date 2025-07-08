import express from "express";
import { router } from "#src/routes/index.js";
import { errorHandler } from "#src/middlewares/errorHandler.js";
import { corsMiddleware } from "#src/middlewares/corsHandler.js";
const app = express();

// Middleware
app.use(corsMiddleware);
app.use(express.json());

// Routes
app.use("/api", router);

app.use(errorHandler);

export default app;
