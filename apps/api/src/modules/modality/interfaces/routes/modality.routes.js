import { Router } from "express";
import { ModalityController } from "#modality/interfaces/controllers/ModalityController.js";

export const modalityRouter = Router();

modalityRouter.get("/", ModalityController.findAll);

modalityRouter.post("/", ModalityController.createModality);
