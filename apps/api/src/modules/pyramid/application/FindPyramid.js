import { Description as RoundDescription } from "#src/modules/round/domain/valueObjects/Description.js";

export class FindPyramid {
  constructor({ pyramidRepo }) {
    this.pyramidRepo = pyramidRepo;
  }

  async execute(pyramidFilters) {
    const matches = await this.pyramidRepo.findPyramid(pyramidFilters);

    const groupedByCategory = matches.reduce((acc, match) => {
      const categoryId = match.category_id;

      if (!acc[categoryId]) {
        acc[categoryId] = {
          details: {
            id: match.category_id,
            initial_age: match.initial_age,
            final_age: match.final_age,
            initial_weight: match.initial_weight,
            final_weight: match.final_weight,
            special_condition: match.special_condition,
            modality: match.modality_description,
            ranks: match.ranks || [],
          },
          rounds: {},
        };
      }

      let roundName = match.round_name;
      if (roundName === RoundDescription.ROUND_OF_16) roundName = "round1";
      if (roundName === RoundDescription.QUARTERFINAL) roundName = "byes";

      if (!acc[categoryId].rounds[roundName]) {
        acc[categoryId].rounds[roundName] = [];
      }

      acc[categoryId].rounds[roundName].push({
        first_competitor: match.first_competitor,
        second_competitor: match.second_competitor,
      });

      return acc;
    }, {});

    // Ordena los enfrentamientos dentro de cada ronda, colocando los byes primero.
    for (const categoryId in groupedByCategory) {
      for (const roundName in groupedByCategory[categoryId].rounds) {
        groupedByCategory[categoryId].rounds[roundName].sort((a, b) => {
          if (a.second_competitor === null && b.second_competitor !== null) {
            return -1; // a (con bye) va primero
          }
          if (a.second_competitor !== null && b.second_competitor === null) {
            return 1; // b (con bye) va primero
          }
          return 0; // Sin cambio en el orden
        });
      }
    }
    return groupedByCategory;
  }
}
