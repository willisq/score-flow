export class Competitor {
	constructor({ id, student, rank, academy, specialCondition }) {
		this.id = id;
		this.student = student;
		this.rank = rank;
		this.academy = academy;
		this.specialCondition = specialCondition;
	}

	toJSON() {
		return {
			id: this.id,
			student: this.student,
			rank: this.rank,
			academy: this.academy,
			special_condition: this.specialCondition.value,
		};
	}
}