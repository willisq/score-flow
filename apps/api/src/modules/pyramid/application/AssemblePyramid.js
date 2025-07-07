import { randomUUID } from "crypto";

import { Description as RoundType } from "#src/modules/round/domain/valueObjects/Description.js";

export class AssemblePyramid {
	constructor({ unitOfWork }) {
		this.unitOfWork = unitOfWork;
	}

	async execute({ championshipId }) {
		return this.unitOfWork.execute(async (repos) => {
			const { competitorRepository, pyramidRepository } = repos;

			await pyramidRepository.deleteAllPyramids();

			const competitorsCategories =
				await competitorRepository.findAllByChampionship(championshipId);

			const competitorOrganizedByCategory = Object.groupBy(
				competitorsCategories,
				(competitorsCategory) => competitorsCategory.category,
			);

			this.#shuffleCompetitorsOnCategories(competitorOrganizedByCategory);

			const pyramidStructure = {};
			for (const categoryId in competitorOrganizedByCategory) {
				const competitors = competitorOrganizedByCategory[categoryId];
				const numberOfCompetitors = competitors.length;

				const numberOfRounds = this.#calculateRounds(numberOfCompetitors);
				const roundTypes = this.#determineRoundTypes(numberOfRounds);
				const firstRoundSetup = this.#generateFirstRound(competitors);

				// Los enfrentamientos ocurren en la primera ronda del torneo.
				const matchesRoundName =
					roundTypes.length > 0 ? roundTypes[0] : RoundType.FINAL;
				// Los competidores con "bye" avanzan directamente a la segunda ronda.
				const byesRoundName = roundTypes.length > 1 ? roundTypes[1] : null;

				const competitorsOnSecondRound = firstRoundSetup.byes.map(
					(competitor) => competitor.firstCompetitor,
				);
				const nextRoundPairs = [];
				for (let i = 0; i < competitorsOnSecondRound.length; i += 2) {
					const pair = {
						firstCompetitor: competitorsOnSecondRound[i],
						secondCompetitor: competitorsOnSecondRound[i + 1] || null,
					};
					nextRoundPairs.push(pair);
				}

				pyramidStructure[categoryId] = {
					numberOfRounds,
					roundTypes,
					firstRound: {
						roundName: matchesRoundName,
						pairs: firstRoundSetup.matches,
					},
					byes: {
						roundName: byesRoundName,
						pairs: nextRoundPairs,
					},
				};
			}

			const dataToPersist = [];
			for (const { firstRound, byes } of Object.values(pyramidStructure)) {
				for (const pairs of firstRound.pairs) {
					dataToPersist.push({
						id: randomUUID(),
						firstCompetitor: pairs.firstCompetitor.id,
						secondCompetitor: pairs.secondCompetitor?.id || null,
						roundName: firstRound.roundName,
					});
				}
				for (const pairs of byes.pairs) {
					dataToPersist.push({
						id: randomUUID(),
						firstCompetitor: pairs.firstCompetitor.id,
						secondCompetitor: pairs.secondCompetitor?.id || null,
						roundName: byes.roundName,
					});
				}
			}

			await pyramidRepository.createBulk(dataToPersist);

			return dataToPersist;
		});
	}

	#shuffleCompetitorsOnCategories(competitorOrganizedByCategory) {
		for (const competitorsOnCategory of Object.values(
			competitorOrganizedByCategory,
		)) {
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
	 * Generates the matches and byes for the first round of the tournament.
	 * @param {Array<object>} competitors - The shuffled list of competitors for a category.
	 * @returns {{matches: Array<object>, byes: Array<object>}} An object containing the matches and byes.
	 */
	#generateFirstRound(competitors) {
		const numberOfCompetitors = competitors.length;
		if (numberOfCompetitors < 2) {
			return { matches: [], byes: [] };
		}

		// Calculate the size of the bracket (next power of 2)
		const bracketSize = 2 ** this.#calculateRounds(numberOfCompetitors);

		// Calculate how many competitors get a bye
		const numberOfByes = bracketSize - numberOfCompetitors;

		// The first N competitors in the shuffled list get a bye
		const competitorsWithBye = competitors.slice(0, numberOfByes);

		const byes = competitorsWithBye.map((competitor) => ({
			firstCompetitor: competitor,
			secondCompetitor: null,
		}));

		// The rest of the competitors will play in the first round
		const competitorsInFirstRound = competitors.slice(numberOfByes);

		const matches = [];
		for (let i = 0; i < competitorsInFirstRound.length; i += 2) {
			const match = {
				firstCompetitor: competitorsInFirstRound[i],
				secondCompetitor: competitorsInFirstRound[i + 1],
			};
			matches.push(match);
		}

		return { matches, byes };
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
