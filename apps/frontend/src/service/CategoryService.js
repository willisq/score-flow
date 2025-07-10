import { api } from "@/service/AxiosBaseService";

export class CategoryService {
  static async getCategories() {
    const { data } = await api.get("/category/");

    return data;
  }

  static async create(categoryData) {
    const { data } = await api.post("/category/", categoryData);

    return data;
  }
}
