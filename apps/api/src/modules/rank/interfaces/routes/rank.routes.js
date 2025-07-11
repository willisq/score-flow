import { Router } from "express";
import { RankController } from "#rank/interfaces/controllers/RankController.js";

const rankRouter = Router();

rankRouter.get("/", RankController.findAll);

rankRouter.post("/", RankController.create);

export { rankRouter };
