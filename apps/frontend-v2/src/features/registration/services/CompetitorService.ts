import { httpClient } from "@/core/api/http-client";
import type {
  Competitor,
  CompetitorCreate,
  CompetitorFilters,
  CompetitorCategoryFilters,
  CompetitorFilterOptions,
} from "../types";

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

  static async update(id: string, payload: CompetitorCreate): Promise<Competitor> {
    const { data } = await httpClient.put<Competitor>(`${this.BASE}/${id}`, payload);
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

  static async getForCategoryBuilder(
    filters: CompetitorCategoryFilters
  ): Promise<Competitor[]> {
    const { data } = await httpClient.get<Competitor[]>(
      `${this.BASE}/for-category-builder`,
      { params: filters }
    );
    return data;
  }

  static async getUnregisteredForCategoryBuilder(
    filters: CompetitorCategoryFilters,
    tournamentId?: string
  ): Promise<Competitor[]> {
    const params: any = { ...filters };
    if (tournamentId) {
      params.tournament_id = tournamentId;
    }
    
    const { data } = await httpClient.get<Competitor[]>(
      `/tournament/competitors/unregistered`,
      { params }
    );
    return data;
  }

  static async getFilterOptions(): Promise<CompetitorFilterOptions> {
    const { data } = await httpClient.get<CompetitorFilterOptions>(
      `${this.BASE}/filter-options`
    );
    return data;
  }
}
