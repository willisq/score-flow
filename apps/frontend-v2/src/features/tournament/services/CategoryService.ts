import { httpClient } from "@/core/api/http-client";
import type { Category, CategoryCreate, CategoryBulkCreate } from "../types";
import type { Competitor } from "@/features/registration/types";

export class CategoryService {
  private static readonly BASE = "/tournament/categories";

  static async getAll(): Promise<Category[]> {
    const { data } = await httpClient.get<Category[]>(this.BASE);
    return data;
  }

  static async create(payload: CategoryCreate): Promise<Category[]> {
    const { data } = await httpClient.post<Category[]>(this.BASE, payload);
    return data;
  }

  static async getCompetitors(categoryModalityId: string): Promise<Competitor[]> {
    const { data } = await httpClient.get<Competitor[]>(
      `${this.BASE}/modalities/${categoryModalityId}/competitors`
    );
    return data;
  }

  static async createBulk(payload: CategoryBulkCreate): Promise<Category[]> {
    const { data } = await httpClient.post<Category[]>(`${this.BASE}/bulk`, payload);
    return data;
  }
}
