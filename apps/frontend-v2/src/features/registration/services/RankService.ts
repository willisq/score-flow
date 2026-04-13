import { httpClient } from "@/core/api/http-client";
import type { Rank, RankCreate } from "../types";

export class RankService {
  private static readonly BASE = "/registration/ranks";

  static async getAll(): Promise<Rank[]> {
    const { data } = await httpClient.get<Rank[]>(this.BASE);
    return data;
  }

  static async create(payload: RankCreate): Promise<Rank> {
    const { data } = await httpClient.post<Rank>(this.BASE, payload);
    return data;
  }
}
