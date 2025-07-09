import { Description as RoundDescription } from "#src/modules/round/domain/valueObjects/Description.js";

export class FindPyramid {
	constructor({ pyramidRepo }) {
		this.pyramidRepo = pyramidRepo;
	}

	async execute(pyramidFilters) {
		const matches = await this.pyramidRepo.findPyramid(pyramidFilters);
		
		const groupedByRound = matches.reduce((acc, match) => {
			let roundName = match.round_name
            if (roundName === RoundDescription.ROUND_OF_16 ) roundName = 'round1';
            if (roundName === RoundDescription.QUARTERFINAL ) roundName = 'byes';

			if (!acc[roundName]) {
				acc[roundName] = [];
			}
			
			acc[roundName].push({
				first_competitor: match.first_competitor,
				second_competitor: match.second_competitor,
			});
			
			return acc;
		}, {});

		// Ordena los enfrentamientos dentro de cada ronda, colocando los byes primero.
		for (const roundName in groupedByRound) {
			groupedByRound[roundName].sort((a, b) => {
				if (a.second_competitor === null && b.second_competitor !== null) {
					return -1; // a (con bye) va primero
				}
				if (a.second_competitor !== null && b.second_competitor === null) {
					return 1; // b (con bye) va primero
				}
				return 0; // Sin cambio en el orden
			});
		}
		return groupedByRound;
	}
}
