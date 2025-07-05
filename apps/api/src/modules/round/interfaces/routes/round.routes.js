import { Router } from "express";
import { RoundController } from "#round/interfaces/controllers/RoundController.js";

const roundRouter = Router();

roundRouter.post("/", RoundController.create);

export { roundRouter };