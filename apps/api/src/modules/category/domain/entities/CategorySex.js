export class CategorySex {
	constructor(categorySexData) {
		const {category, sex} = categorySexData;

		this.category = category;
		this.sex = sex;
	}

	toJSON() {
		return {
			category: this.category,
			sex: this.sex,
		};
	}
}
