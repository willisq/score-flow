import { Router } from "express";
import { RankController } from "#rank/interfaces/controllers/RankController.js";

const rankRouter = Router();

rankRouter.post("/", RankController.create);

export { rankRouter };