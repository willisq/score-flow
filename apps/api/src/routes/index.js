import { Router } from "express";
import { PersonRouter } from "#person/interfaces/routes/person.routes.js";
import { AcademyRouter } from "#academy/interfaces/routes/academy.routes.js";
import { rankRouter } from "#rank/interfaces/routes/rank.routes.js";
import { competitorRouter } from "#competitor/interfaces/routes/competitor.routes.js";
import { modalityRouter } from "#modality/interfaces/routes/modality.routes.js";
import { roundRouter } from "#round/interfaces/routes/round.routes.js";
import { sexRouter } from "#sex/interfaces/routes/sex.routes.js";

export const router = Router();

router.use("/person", PersonRouter);
router.use("/academy", AcademyRouter);
router.use("/rank", rankRouter);
router.use("/competitor", competitorRouter);
router.use("/modality", modalityRouter);
router.use("/round", roundRouter);
router.use("/sex", sexRouter);
