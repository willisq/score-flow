import { Router } from "express";
import { CompetitorController } from "#competitor/interfaces/controllers/CompetitorController.js";

const competitorRouter = Router();

competitorRouter.post("/", CompetitorController.create);

export { competitorRouter };