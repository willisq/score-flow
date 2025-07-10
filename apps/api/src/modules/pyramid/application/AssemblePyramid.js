import { randomUUID } from "crypto";

import { CompetitorCategory } from "#src/modules/competitor/domain/entities/CompetitorCategory.js";

import { Description as RoundType } from "#src/modules/round/domain/valueObjects/Description.js";

export class AssemblePyramid {
  constructor({ unitOfWork }) {
    this.unitOfWork = unitOfWork;
  }

  async execute({ championship, category }) {
    return this.unitOfWork.execute(async (repos) => {
      const { competitorRepository, pyramidRepository } = repos;

      await pyramidRepository.deletePyramidByCategory(category);

      const competitorsCategories =
        await competitorRepository.findCompetitorCategory({
          championship,
          category,
        });
      const numberOfCompetitors = competitorsCategories.length;

      const competitorsOrganizedByAcademy = Object.groupBy(
        competitorsCategories,
        (competitorsCategory) => competitorsCategory.academy
      );

      const academyNames = Object.keys(competitorsOrganizedByAcademy);

      this.#shuffleCompetitorsOnCategories(competitorsOrganizedByAcademy);

      const pairs = [];
      const competitorsOnPyramid = new Set();

      while (competitorsOnPyramid.size < numberOfCompetitors) {
        let first = null,
          second = null;

        for (let academyName of academyNames) {
          const competitorsOnAcademy =
            competitorsOrganizedByAcademy[academyName];
          for (let competitor of competitorsOnAcademy) {
            if (!competitorsOnPyramid.has(competitor.id)) {
              first = competitor;
              break;
            }
          }
          if (first) break;
        }
        if (!first) break;

        for (let academyName of academyNames) {
          const competitorsOnAcademy =
            competitorsOrganizedByAcademy[academyName];
          for (let competitor of competitorsOnAcademy) {
            if (
              !competitorsOnPyramid.has(competitor.id) &&
              competitor.academy !== first.academy
            ) {
              second = competitor;
              break;
            }
          }
          if (second) break;
        }

        if (!second) {
          for (const competitor of competitorsCategories) {
            if (
              !competitorsOnPyramid.has(competitor.id) &&
              competitor.id !== first.id
            ) {
              second = competitor;
              break;
            }
          }
        }

        if (second) {
          pairs.push({
            first: new CompetitorCategory(first),
            second: new CompetitorCategory(second),
          });
          competitorsOnPyramid.add(first.id);
          competitorsOnPyramid.add(second.id);
        } else {
          pairs.push({
            first: new CompetitorCategory(first),
            second: null,
          });
          competitorsOnPyramid.add(first.id);
        }
      }

      const numberOfRounds = this.#calculateRounds(numberOfCompetitors);
      const roundTypes = this.#determineRoundTypes(numberOfRounds);

      const numberOfPairs = pairs.length;
      let indexOfPower = 1;
      while (indexOfPower < numberOfPairs) {
        indexOfPower *= 2;
      }

      const byesCount = indexOfPower - numberOfPairs;

      const pairsWithRound = pairs.map((pair, index) => {
        if (numberOfPairs - index <= byesCount) {
          return {
            id: randomUUID(),
            firstCompetitor: pair.first.id,
            secondCompetitor: pair.second?.id ?? null,
            roundName: roundTypes.length > 0 ? roundTypes[1] : RoundType.FINAL,
          };
        } else {
          return {
            id: randomUUID(),
            firstCompetitor: pair.first.id,
            secondCompetitor: pair.second?.id ?? null,
            roundName: roundTypes.length > 0 ? roundTypes[0] : RoundType.FINAL,
          };
        }
      });

      await pyramidRepository.createBulk(pairsWithRound);

      return pairsWithRound;
    });
  }

  #shuffleCompetitorsOnCategories(organizedCompetitors) {
    for (const competitorsOnCategory of Object.values(organizedCompetitors)) {
      for (let i = competitorsOnCategory.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [competitorsOnCategory[i], competitorsOnCategory[j]] = [
          competitorsOnCategory[j],
          competitorsOnCategory[i],
        ];
      }
    }
  }

  /**
   * Calculates the number of rounds needed for a given number of competitors.
   * Uses the formula ceil(log2(n)), where n is the number of competitors.
   * @param {number} competitorCount The number of competitors.
   * @returns {number} The total number of rounds.
   */
  #calculateRounds(competitorCount) {
    if (competitorCount < 2) return 0;
    // Math.ceil(Math.log2(N))
    return Math.ceil(Math.log2(competitorCount));
  }

  /**
   * Determines the names of the rounds based on the total number of rounds.
   * @param {number} numberOfRounds The total number of rounds.
   * @returns {string[]} An array of round descriptions.
   */
  #determineRoundTypes(numberOfRounds) {
    const roundMap = {
      1: [RoundType.FINAL],
      2: [RoundType.SEMIFINAL, RoundType.FINAL],
      3: [RoundType.QUARTERFINAL, RoundType.SEMIFINAL, RoundType.FINAL],
      4: [
        RoundType.ROUND_OF_16,
        RoundType.QUARTERFINAL,
        RoundType.SEMIFINAL,
        RoundType.FINAL,
      ],
      5: [
        RoundType.ROUND_OF_32,
        RoundType.ROUND_OF_16,
        RoundType.QUARTERFINAL,
        RoundType.SEMIFINAL,
        RoundType.FINAL,
      ],
    };

    // Devuelve las rondas desde la más temprana a la final
    return roundMap[numberOfRounds] || [];
  }
}
