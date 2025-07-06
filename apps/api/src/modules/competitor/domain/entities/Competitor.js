export class Competitor {
	constructor({
		id,
		student,
		rank,
		academy,
		specialCondition,
		sex,
		weight = null,
		age = null,
		height = null,
	}) {
		this.id = id;
		this.student = student;
		this.rank = rank;
		this.academy = academy;
		this.specialCondition = specialCondition;
		this.weight = weight;
		this.age = age;
		this.height = height;
		this.sex = sex;
	}

	toJSON() {
		return {
			id: this.id,
			student: this.student,
			rank: this.rank,
			sex: this.sex,
			academy: this.academy,
			special_condition: this.specialCondition.value,
			weight: this.weight.value,
			age: this.age.value,
			height: this.height.value,
		};
	}
}
