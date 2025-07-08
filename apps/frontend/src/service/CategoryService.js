import { api } from "@/service/AxiosBaseService";

export class CategoryService {
	static async getCategories() {
		const { data } = await api.get("/category/");

		return data;
	}
}
