import { Router } from "express";
import { CategoryController } from "#category/interfaces/controllers/CategoryController.js";
import { CategorySexController } from "#category/interfaces/controllers/CategorySexController.js";
const categoryRouter = Router();

categoryRouter.get("/", CategoryController.findAll);

categoryRouter.post("/", CategoryController.create);
categoryRouter.post("/sexes", CategorySexController.create);

export { categoryRouter };
