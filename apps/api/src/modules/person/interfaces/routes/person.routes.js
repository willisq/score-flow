import {Router} from "express";
import {PersonController} from "#person/interfaces/controllers/PersonController.js";

export const PersonRouter = Router();

PersonRouter.post("/", PersonController.createPerson);