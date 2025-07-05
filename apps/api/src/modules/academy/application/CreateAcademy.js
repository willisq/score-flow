import { randomUUID } from "crypto";

import { Academy } from "#academy/domain/entities/Academy.js";
import { Name } from "#academy/domain/valueObjects/Name.js";

export class CreateAcademy {
  constructor({ academyRepository }) {
    this.academyRepository = academyRepository;
  }

  async execute({ name, instructorId }) {
    const academy = new Academy({
      id: randomUUID(),
      name: new Name(name),
      instructor: instructorId,
    });

    return await this.academyRepository.create(academy);
  }
}
