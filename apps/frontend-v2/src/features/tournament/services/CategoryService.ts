import { httpClient } from "@/core/api/http-client";
import type { Category, CategoryCreate, CategoryBulkCreate, CategoryUpdate } from "../types";
import type { Competitor } from "@/features/registration/types";

export class CategoryService {
  private static readonly BASE = "/tournament/categories";

  static async getAll(hasCompetitors?: boolean | null): Promise<Category[]> {
    const { data } = await httpClient.get<Category[]>(this.BASE, {
      params: hasCompetitors != null ? { has_competitors: hasCompetitors } : {}
    });
    return data;
  }

  static async create(payload: CategoryCreate): Promise<Category[] | Category> {
    const { data } = await httpClient.post<Category[] | Category>(this.BASE, payload);
    return data;
  }

  static async update(id: string, payload: CategoryUpdate): Promise<Category> {
    const { data } = await httpClient.patch<Category>(`${this.BASE}/${id}`, payload);
    return data;
  }

  static async updateModality(id: string, payload: any): Promise<any> {
    const { data } = await httpClient.patch<any>(`${this.BASE}/modalities/${id}`, payload);
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
