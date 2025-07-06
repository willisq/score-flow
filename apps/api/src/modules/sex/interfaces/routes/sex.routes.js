import { Router } from "express";
import { SexController } from "#sex/interfaces/controllers/SexController.js";

const sexRouter = Router();

sexRouter.post("/", SexController.create);

export { sexRouter };