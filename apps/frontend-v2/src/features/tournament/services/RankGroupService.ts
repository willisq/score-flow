import { httpClient } from "@/core/api/http-client";
import type { RankGroup, RankGroupCreate, RankGroupUpdate } from "../types";

export class RankGroupService {
  private static readonly BASE = "/tournament/rank-groups";

  static async getAll(): Promise<RankGroup[]> {
    const { data } = await httpClient.get<RankGroup[]>(this.BASE);
    return data;
  }

  static async getById(id: string): Promise<RankGroup> {
    const { data } = await httpClient.get<RankGroup>(`${this.BASE}/${id}`);
    return data;
  }

  static async create(payload: RankGroupCreate): Promise<RankGroup> {
    const { data } = await httpClient.post<RankGroup>(this.BASE, payload);
    return data;
  }

  static async update(id: string, payload: RankGroupUpdate): Promise<RankGroup> {
    const { data } = await httpClient.patch<RankGroup>(`${this.BASE}/${id}`, payload);
    return data;
  }

  static async delete(id: string): Promise<void> {
    await httpClient.delete(`${this.BASE}/${id}`);
  }
}
