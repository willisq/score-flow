import { databaseService } from "#src/services/database/databaseService.js";

import { CreateSex } from "#sex/application/CreateSex.js";
import { FindAllSexes } from "#sex/application/FindAllSexes.js";

import { SexDatabaseRepository } from "#sex/infraestructure/SexDatabaseRepository.js";

export class SexController {
  static async create(req, res) {
    const repo = new SexDatabaseRepository(databaseService);
    const useCase = new CreateSex({ repository: repo });

    const sex = await useCase.execute(req.body);

    return res.status(201).json(sex);
  }

  static async findAll(_, res) {
    const repo = new SexDatabaseRepository(databaseService);
    const useCase = new FindAllSexes({ sexRepository: repo });

    const sexes = await useCase.execute();

    return res.status(200).json(sexes);
  }
}
