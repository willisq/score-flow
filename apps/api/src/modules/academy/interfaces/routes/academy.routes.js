import {Router} from "express";
import {AcademyController} from "#academy/interfaces/controllers/AcademyController.js";

export const AcademyRouter = Router();

AcademyRouter.post("/", AcademyController.createAcademy);
AcademyRouter.get("/", AcademyController.getAll);