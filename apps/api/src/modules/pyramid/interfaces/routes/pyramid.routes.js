import { Router } from "express";

import { PyramidController } from "#pyramid/interfaces/controllers/PyramidController.js";

const pyramidRouter = Router();

pyramidRouter.post("/", PyramidController.create);

export { pyramidRouter };