import { Router } from "express";
import { CompetitorController } from "#competitor/interfaces/controllers/CompetitorController.js";

const competitorRouter = Router();

competitorRouter.get("/", CompetitorController.findAll);
competitorRouter.get(
  "/by-category-and-championship",
  CompetitorController.findByCategory
);

competitorRouter.post("/", CompetitorController.create);

export { competitorRouter };
