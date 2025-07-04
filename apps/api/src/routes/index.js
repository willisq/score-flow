import { Router } from "express";
import { PersonRouter } from "#person/interfaces/routes/person.routes.js";

export const router = Router();

router.use("/person", PersonRouter);
