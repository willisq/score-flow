import { httpClient } from "@/core/api/http-client";
import type { Sex, SexCreate } from "../types";

export class SexService {
  private static readonly BASE = "/registration/sexes";

  static async getAll(): Promise<Sex[]> {
    const { data } = await httpClient.get<Sex[]>(this.BASE);
    return data;
  }

  static async create(payload: SexCreate): Promise<Sex> {
    const { data } = await httpClient.post<Sex>(this.BASE, payload);
    return data;
  }
}
