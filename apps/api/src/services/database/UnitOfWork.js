import { CategoryDatabaseRepository } from "#category/infraestructure/CategoryDatabaseRepository.js";
import { CategoryRankDatabaseRepository } from "#category/infraestructure/CategoryRankDatabaseRepository.js";
import { CategorySexDatabaseRepository } from "#category/infraestructure/CategorySexDatabaseRepository.js";

export class UnitOfWork {
	constructor({ databaseService, repositoriesClasses }) {
		this.databaseService = databaseService;
		this.repositoriesClasses = repositoriesClasses;
	}

	/**
	 * Executes a given piece of work within a single database transaction.
	 * @param {Function} work - The async function to execute. It will receive an object
	 * with instances of all repositories configured for the transaction.
	 * @returns The result of the work function.
	 */
	async execute(work) {
		return this.databaseService.transaction(async (trx) => {
			const repositories = {};
			for (const [repositoryName, repositoryClass] of Object.entries(
				this.repositoriesClasses,
			)) {
				repositories[repositoryName] = new repositoryClass({
					databaseService: trx,
				});
			}

			return work(repositories);
		});
	}
}
