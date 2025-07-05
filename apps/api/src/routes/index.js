import { Router } from "express";
import { PersonRouter } from "#person/interfaces/routes/person.routes.js";
import { AcademyRouter } from "#academy/interfaces/routes/academy.routes.js";
import { rankRouter } from "#rank/interfaces/routes/rank.routes.js";

export const router = Router();

router.use("/person", PersonRouter);
router.use("/academy", AcademyRouter);
router.use("/rank", rankRouter);
