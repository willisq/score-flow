import { httpClient } from "@/core/api/http-client";
import type { Tournament, TournamentCreate } from "../types";

export class TournamentService {
  private static readonly BASE = "/tournament/tournaments";

  static async getAll(): Promise<Tournament[]> {
    const { data } = await httpClient.get<Tournament[]>(this.BASE);
    return data;
  }

  static async create(payload: TournamentCreate): Promise<Tournament> {
    const { data } = await httpClient.post<Tournament>(this.BASE, payload);
    return data;
  }
}
