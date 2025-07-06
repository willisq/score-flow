export class CategorySex {
	constructor(categorySexData) {
        Object.assign(this, categorySexData);
	}

	toJSON() {
		return {
			category: this.category,
			sex: this.sex,
		};
	}
}
