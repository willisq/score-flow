import { randomUUID } from "crypto";

import { Person } from "#person/domain/entities/Person.js";
import { Firstname } from "#person/domain/valuesObjects/Firstname.js";
import { Lastname } from "#person/domain/valuesObjects/Lastname.js";
import { Competitor } from "#competitor/domain/entities/Competitor.js";

import { Weight } from "#competitor/domain/valueObjects/Weight.js";
import { Age } from "#competitor/domain/valueObjects/Age.js";
import { Height } from "#competitor/domain/valueObjects/Height.js";
import { SpecialCondition } from "#competitor/domain/valueObjects/SpecialCondition.js";

import { CategoryAge } from "#category/domain/valueObjects/CategoryAge.js";
import { CategoryHeight } from "#category/domain/valueObjects/CategoryHeight.js";
import { CategorySpecialCondition } from "#category/domain/valueObjects/CategorySpecialCondition.js";
import { CategoryWeight } from "#category/domain/valueObjects/CategoryWeight.js";

export class CreateBulkCompetitors {
  constructor({ unitOfWork }) {
    this.unitOfWork = unitOfWork;
  }

  async execute(competitorsData) {
    if (!Array.isArray(competitorsData) || competitorsData.length === 0) {
      throw new Error("Input must be a non-empty array of competitors.");
    }

    return this.unitOfWork.execute(async (repos) => {
      const createdRecords = await Promise.all(
        competitorsData.map(async (data) => {
          const {
            personData,
            rank,
            sex,
            academy,
            weight,
            height = null,
            age,
            championship,
            specialCondition = false,
            modalities,
          } = data;

          const person = new Person({
            id: randomUUID(),
            firstname: new Firstname(personData.firstname),
            lastname: new Lastname(personData.lastname),
          });
          const createdPerson = await repos.personRepository.create(person);

          const competitor = new Competitor({
            id: randomUUID(),
            student: createdPerson.id,
            rank,
            sex,
            academy,
            specialCondition: new SpecialCondition(specialCondition),
            height: new Height(height),
            weight: new Weight(weight),
            age: new Age(age),
          });
          const createdCompetitor = await repos.competitorRepository.create(
            competitor
          );

          for (const modality of modalities) {
            const category = await repos.categoryRepository.findCategory({
              rank: createdCompetitor.rank,
              weight: new CategoryWeight(competitor.weight.value),
              age: new CategoryAge(competitor.age.value),
              height: new CategoryHeight(competitor.height.value),
              sex: createdCompetitor.sex,
              modality,
              specialCondition: new CategorySpecialCondition(
                competitor.specialCondition.value
              ),
            });

            if (!category)
              throw new Error("No hay categoria creada para el competidor");

            await repos.categoryRepository.addCompetitorOnCategory({
              id: randomUUID(),
              competitor,
              category,
              championship,
            });
          }

          return { ...createdCompetitor, person: createdPerson };
        })
      );

      return createdRecords;
    });
  }
}
