import { Router } from "express";

import { PyramidController } from "#pyramid/interfaces/controllers/PyramidController.js";

const pyramidRouter = Router();

pyramidRouter.get("/", PyramidController.findPyramid);

pyramidRouter.post("/", PyramidController.create);

export { pyramidRouter };