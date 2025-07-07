export class PyramidRepository {
	constructor({ databaseService }) {
		this.databaseService = databaseService;
	}

	async createBulk(matches) {
		throw new Error("Method not implemented.");
	}

	async deleteAllPyramids() {
		throw new Error("Method not implemented.");
	}
}
