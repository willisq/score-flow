import { httpClient } from "@/core/api/http-client";
import type { Category, CategoryCreate } from "../types";

export class CategoryService {
  private static readonly BASE = "/tournament/categories";

  static async getAll(): Promise<Category[]> {
    const { data } = await httpClient.get<Category[]>(this.BASE);
    return data;
  }

  static async create(payload: CategoryCreate): Promise<Category> {
    const { data } = await httpClient.post<Category>(this.BASE, payload);
    return data;
  }
}
