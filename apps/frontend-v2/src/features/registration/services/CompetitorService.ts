import { httpClient } from "@/core/api/http-client";
import type { Competitor, CompetitorCreate, CompetitorFilters } from "../types";

export class CompetitorService {
  private static readonly BASE = "/registration/competitors";

  static async getAll(filters?: CompetitorFilters): Promise<Competitor[]> {
    const { data } = await httpClient.get<Competitor[]>(this.BASE, { params: filters });
    return data;
  }

  static async create(payload: CompetitorCreate): Promise<Competitor> {
    const { data } = await httpClient.post<Competitor>(this.BASE, payload);
    return data;
  }

  static async createBulk(competitors: CompetitorCreate[]): Promise<Competitor[]> {
    const { data } = await httpClient.post<Competitor[]>(`${this.BASE}/bulk`, { competitors });
    return data;
  }

  static async uploadExcel(file: File): Promise<Competitor[]> {
    const formData = new FormData();
    formData.append("file", file);
    const { data } = await httpClient.post<Competitor[]>(`${this.BASE}/upload`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return data;
  }

  static async downloadTemplate(): Promise<Blob> {
    const { data } = await httpClient.get<Blob>(`${this.BASE}/template`, {
      responseType: "blob",
    });
    return data;
  }
}
