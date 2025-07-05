import { Router } from "express";
import { ModalityController } from "#modality/interfaces/controllers/ModalityController.js";

export const modalityRouter = Router();

modalityRouter.post("/", ModalityController.createModality);