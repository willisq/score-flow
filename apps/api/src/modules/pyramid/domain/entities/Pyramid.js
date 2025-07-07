export class Pyramid {
	constructor({
		id,
		round,
		firstCompetitor,
		secondCompetitor = null,
		winner = null,
	}) {
		this.id = id;
		this.round = round;
		this.firstCompetitor = firstCompetitor;
		this.secondCompetitor = secondCompetitor;
		this.winner = winner;
	}

    toJSON(){
        return {
            id: this.id,
            round: this.round,
            firstCompetitor: this.firstCompetitor,
            secondCompetitor: this.secondCompetitor,
            winner: this.winner
        };
        
    }
}
